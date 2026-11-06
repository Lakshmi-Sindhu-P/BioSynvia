"""Reproducible pre-modeling protocol artifacts; deliberately contains no fitting."""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
import io
import json
from pathlib import Path
import platform
import shutil
import sqlite3
import sys
import zipfile
import csv

import numpy as np
import openpyxl
from openpyxl.utils import get_column_letter
import pandas as pd

from .preparation import CORE_FIELDS, TARGET, feature_id, fingerprint
from .source import inventory_archive

FIVE = CORE_FIELDS[:5]
TOL = 1e-10
CONTRACTS = ['target_decision', 'inference_contract', 'data_quality_policy', 'split_protocol', 'benchmark_protocol', 'issue_register']
SHEET_FAMILIES = ('inline_CO2', 'inline_Turbidity', 'inline_Permittivity',
                  'inline_ProcessParameters', 'online_NaOH', 'online_Feed',
                  'offline_CellAnalysis', 'offline_MediumAnalysis')
EXPECTED_SHEETS = {f'{reactor}_{family}' for reactor in ('R01', 'R02') for family in SHEET_FAMILIES}
ALIGNED_INLINE_HEADERS = ('Time (h)', 'Dissolved CO2 (%-sat)', 'Transmission (arb. Unit)',
    'Reflection (arb. Unit)', 'Conductivity (mS/cm)', 'Permittivity (pF/cm)', 'fc (kHz)',
    'DeltaEps (pF/cm)', 'Alpha', 'Fitting Quality (Cole fit R2)', 'Fitting Error (Cole fit RMSE)',
    'C (300kHz)', 'C (374kHz)', 'C (466kHz)', 'C (580kHz)', 'C (720kHz)', 'C (896kHz)',
    'C (1118kHz)', 'C (1392kHz)', 'C (1729kHz)', 'C (2155kHz)', 'C (2689kHz)',
    'C (3347kHz)', 'C (4158kHz)', 'C (5188kHz)', 'C (6447kHz)', 'C (8030kHz)',
    'C (9995kHz)', 'pH', 'Dissolved O2 (% air sat)', 'Temperature (°C)',
    'Agitation rate (rpm)', 'Aeration rate total (sL/h)', 'O2 fraction inlet (%)',
    'CO2 fraction inlet (%)', 'Aeration rate air (sL/h)', 'Aeration rate O2 (sL/h)',
    'Aeration rate CO2 (sL/h)', 'Liquid volume (L)', 'Cumulative NaOH weight (g)',
    'Cumulative feed weight (g)')
ALIGNED_OFFLINE_HEADERS = ('Time (h)', 'VCD Mean (cells/mL)', 'VCD SEM (cells/mL)',
    'TCD Mean (cells/mL)', 'TCD SEM (cells/mL)', 'Viability Mean (%)', 'Viability SEM (%)',
    'Avg. diameter Mean (µm)', 'Avg. diameter SEM (µm)', 'Avg. compactness Mean',
    'Avg. compactness SEM', 'Aggregation Mean (%)', 'Aggregation SEM (%)', 'Glucose (g/L)',
    'Lactate (g/L)', 'Ammonium (mM)', 'Osmolality (mOsmol/kg)')


def json_dumps(value, **kwargs):
    return json.dumps(value, default=lambda item: item.item() if isinstance(item, np.generic) else str(item), **kwargs)


def write_json(path, value):
    path.write_text(json_dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def read_sheet(sheet):
    """Keep physical Excel coordinates even across blank rows."""
    iterator = sheet.iter_rows()
    headers = [cell.value for cell in next(iterator)]
    rows = []
    for row_number, cells in enumerate(iterator, start=2):
        if all(cell.value is None for cell in cells):
            continue
        row = {header: cell.value for header, cell in zip(headers, cells)}
        row['_excel_row'] = row_number
        row['_cell_types'] = {header: cell.data_type for header, cell in zip(headers, cells)}
        rows.append(row)
    return pd.DataFrame(rows), headers


def cutoff_mask(acquisition, availability, cutoff, assume_acquisition=False):
    """Strict unknown/delayed availability is excluded; exact cutoff is included."""
    acquired = np.asarray(acquisition, dtype=float)
    available = acquired if assume_acquisition else np.asarray(availability, dtype=float)
    return np.isfinite(acquired) & np.isfinite(available) & (acquired <= cutoff + TOL) & (available <= cutoff + TOL)


def snapshot_flags(frame, headers, cutoff, age_minutes=5):
    """All independent flags use the acquired prefix only; no fallback to older Ok."""
    times = pd.to_numeric(frame['Time (h)'], errors='coerce').to_numpy(float)
    prefix = frame.loc[np.isfinite(times) & (times <= cutoff + TOL)].copy()
    prefix['_numeric_time'] = times[np.isfinite(times) & (times <= cutoff + TOL)]
    prefix = prefix.sort_values(['_numeric_time', '_excel_row'], kind='stable')
    row = prefix.iloc[-1] if len(prefix) else None
    same = prefix[prefix._numeric_time.eq(row['_numeric_time'])] if row is not None else prefix
    status_present = 'Status' in headers
    status = row['Status'] if row is not None and status_present else None
    fields = [field for field in headers if field not in ('Time (h)', 'Status')]
    rows = []
    for field in fields:
        column = get_column_letter(headers.index(field) + 1)
        numeric = pd.to_numeric(prefix[field], errors='coerce')
        value = pd.to_numeric(pd.Series([row[field] if row is not None else None]), errors='coerce').iloc[0]
        valid = pd.notna(value) and np.isfinite(value)
        derived = field.startswith(('C (', 'fc (', 'Alpha', 'DeltaEps', 'Fitting '))
        age = float(cutoff - row['_numeric_time']) if row is not None else None
        flags = {'no_past_observation': row is None, 'duplicate_source_time': len(same) > 1,
                 'invalid_value': not valid, 'stale': age is not None and age > age_minutes / 60 + TOL,
                 'status_column_absent': not status_present,
                 'status_value_blank': status_present and (status is None or pd.isna(status)),
                 'status_not_ok': status_present and pd.notna(status) and status != 'Ok',
                 'past_only_derived_zero': derived and len(numeric) > 0 and numeric.notna().all() and np.isfinite(numeric).all() and numeric.eq(0).all(),
                 'availability_unknown': True}
        quality_flags = [key for key, flag in flags.items() if flag and key != 'availability_unknown']
        eligible = not quality_flags
        candidates = [{'excel_row':int(candidate['_excel_row']), 'value_cell':f'{column}{int(candidate["_excel_row"])}',
                       'raw_value':None if pd.isna(candidate[field]) else candidate[field],
                       'status':None if not status_present or pd.isna(candidate['Status']) else candidate['Status']}
                      for _, candidate in same.iterrows()] if len(same)>1 else []
        raw = row[field] if row is not None else None
        rows.append({'field':field, 'feature':feature_id(field), 'source_value':float(value) if valid and len(same)==1 else None,
                     'raw_value_json':json_dumps(None if raw is None or pd.isna(raw) else raw),
                     'source_excel_row':int(row['_excel_row']) if row is not None and len(same)==1 else None,
                     'source_cell':f'{column}{int(row["_excel_row"])}' if row is not None and len(same)==1 else None,
                     'source_time_cell':f'A{int(row["_excel_row"])}' if row is not None and len(same)==1 else None,
                     'source_status_cell':f'{get_column_letter(headers.index("Status")+1)}{int(row["_excel_row"])}' if row is not None and status_present and len(same)==1 else None,
                     'source_status':None if status is None or pd.isna(status) else str(status),
                     'source_candidates_json':json_dumps(candidates,sort_keys=True), 'acquisition_time_hours':float(row['_numeric_time']) if row is not None else None,
                     'availability_time_hours':None, 'availability_evidence':'unknown', 'cutoff_hours':float(cutoff), 'age_hours':age,
                     **{key:bool(value) for key,value in flags.items()}, 'quality_reasons_json':json_dumps(quality_flags),
                     'assumed_acquisition_eligible':eligible, 'strict_availability_eligible':False,
                     'proposed_value':float(value) if eligible else None})
    return rows


def proposed_split(coverage):
    """Only design/coverage columns are consumed, never target values or flags."""
    needed = ['experiment_id','reactor_id','process_mode','assays','five_complete']
    data = coverage[needed].copy()
    if data.duplicated(['experiment_id','reactor_id']).any():
        raise ValueError('Duplicate experiment/reactor coverage.')
    records = []
    for experiment, frame in data.groupby('experiment_id',sort=True):
        if set(frame.reactor_id) != {'R01','R02'} or frame.process_mode.nunique()!=1 or (frame.assays<=0).any():
            raise ValueError('Each experiment needs both reactors, one mode and positive denominator.')
        if (frame.five_complete<0).any() or (frame.five_complete>frame.assays).any():
            raise ValueError('Invalid coverage numerator.')
        score = min(Fraction(int(r.five_complete),int(r.assays)) for r in frame.itertuples())
        records.append({'experiment_id':experiment,'process_mode':frame.process_mode.iloc[0], 'score':score,
                        'score_numerator':score.numerator,'score_denominator':score.denominator})
    if {r['process_mode'] for r in records}!={'batch','fed-batch'}:
        raise ValueError('Need both modes for this holdout proposal.')
    tests=[]
    for mode in ['batch','fed-batch']:
        candidates=[r for r in records if r['process_mode']==mode]
        tests.append(sorted(candidates,key=lambda r:(-r['score'],r['experiment_id']))[0]['experiment_id'])
    dev=sorted(r['experiment_id'] for r in records if r['experiment_id'] not in tests)
    if len(dev)<3:
        raise ValueError('Insufficient development groups for outer and inner grouped folds.')
    folds=[]
    for held in dev:
        train=[g for g in dev if g!=held]
        folds.append({'validation':[held],'train':train,'inner_folds':[{'validation':[g],'train':[t for t in train if t!=g]} for g in train]})
    for record in records:
        record.pop('score')
        record['partition']='final_test_proposal' if record['experiment_id'] in tests else 'development'
    return {'split_id':'stage12_coverage_proposal_v1','approved':False,'model_fit_permitted':False,'test_groups':sorted(tests),
            'development_groups':dev,'assignments':records,'outer_development_folds':folds}


def verify_bundle(output):
    """Verify payload bytes and CSV/SQLite logical agreement before promotion."""
    output=Path(output)
    manifest=json.loads((output/'stage12_manifest.json').read_text())
    for name,digest in manifest['outputs'].items():
        if not (output/name).is_file() or fingerprint(output/name)!=digest:
            raise ValueError(f'Artifact hash mismatch: {name}')
    with sqlite3.connect(f'file:{output / "biosynvia.sqlite"}?mode=ro',uri=True) as connection:
        if connection.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
            raise ValueError('SQLite integrity failure')
        for name in manifest['tables']:
            text_columns={row[1]:str for row in connection.execute(f'PRAGMA table_info("{name}")') if row[2]=='TEXT'}
            csv=pd.read_csv(output/f'{name}.csv',dtype=text_columns,keep_default_na=False,na_values=[''],float_precision='round_trip')
            sql=pd.read_sql_query(f'SELECT * FROM "{name}"',connection)
            pd.testing.assert_frame_equal(csv,sql,check_dtype=False,check_exact=False,rtol=1e-12,atol=1e-12)
    return manifest


def assert_original_assays(decisions, origins):
    """Require exact parsed source values/nulls; no CSV-parser drift in labels."""
    for row in origins.itertuples(index=False):
        if row.field not in decisions.columns:
            continue
        actual = decisions.loc[decisions.assay_id.eq(row.assay_id), row.field].iloc[0]
        if not ((pd.isna(actual) and pd.isna(row.value)) or actual == row.value):
            raise ValueError(f'Original assay value changed: {row.assay_id}/{row.field}')


def assert_source_schema(archive, source):
    """Require publisher filenames, exact CSV headers, and 16 named sheets per workbook."""
    inventory = []
    with zipfile.ZipFile(archive) as z:
        for item in source['files']:
            path = item['path']
            if path.endswith('.xlsx'):
                workbook = openpyxl.load_workbook(io.BytesIO(z.read(path)), read_only=True, data_only=False)
                actual = set(workbook.sheetnames)
                if actual != EXPECTED_SHEETS:
                    missing, unexpected = sorted(EXPECTED_SHEETS - actual), sorted(actual - EXPECTED_SHEETS)
                    raise ValueError(f'Workbook sheet schema mismatch for {path}: missing={missing}; unexpected={unexpected}')
                inventory.append({'source_path':path, 'source_kind':'workbook', 'run_id':None,
                                  'schema_role':'raw_authority', 'column_count':None,
                                  'headers_json':json_dumps(sorted(actual)), 'sheet_count':len(actual)})
                workbook.close()
            elif path.endswith('.csv'):
                header = tuple(next(csv.reader(io.TextIOWrapper(z.open(path), encoding='utf-8'))))
                expected = ALIGNED_INLINE_HEADERS if item['measurement_kind'] == 'inline' else ALIGNED_OFFLINE_HEADERS
                if header != expected:
                    raise ValueError(f'Aligned CSV schema mismatch for {path}')
                inventory.append({'source_path':path, 'source_kind':'aligned_csv',
                                  'run_id':f'{item["experiment_id"]}_{item["reactor_id"]}',
                                  'schema_role':'publisher_aligned_candidate_features' if item['measurement_kind'] == 'inline' else 'publisher_aligned_convenience_assays',
                                  'column_count':len(header), 'headers_json':json_dumps(header), 'sheet_count':None})
    if sum(row['source_kind'] == 'workbook' for row in inventory) != 12 or sum(row['source_kind'] == 'aligned_csv' for row in inventory) != 48:
        raise ValueError('Expected exactly 12 workbooks and 48 aligned CSVs.')
    return inventory


def build(archive, parent, output, config_directory=Path('configs'), command=None):
    archive,parent,output,config_directory=map(Path,(archive,parent,output,config_directory))
    stage=output.with_name(output.name+'.incomplete')
    if output.exists() or stage.exists():
        raise ValueError('Choose a new versioned output; existing or incomplete outputs are preserved.')
    source=inventory_archive(archive)
    source_schema=assert_source_schema(archive, source)
    parent_manifest=json.loads((parent/'preparation_manifest.json').read_text())
    if source['sha256']!=parent_manifest['source_sha256']:
        raise ValueError('Parent/source mismatch')
    backup=Path(parent_manifest['backup_path'])
    if fingerprint(backup)!=source['sha256']:
        raise ValueError('Backup hash mismatch')
    consumed={str(parent/'preparation_manifest.json'):fingerprint(parent/'preparation_manifest.json')}
    for name,entry in parent_manifest['outputs'].items():
        path=parent/name
        if fingerprint(path)!=entry['sha256']:
            raise ValueError(f'Parent artifact hash mismatch: {name}')
        consumed[str(path)]=entry['sha256']
    for name in CONTRACTS:
        path=config_directory/f'{name}.json'
        contract=json.loads(path.read_text())
        if contract['model_fit_permitted'] or contract['scientific_approved'] or contract['owner_protocol_approved']:
            raise ValueError('Stage12 requires pending approval contracts.')
        consumed[str(path)]=fingerprint(path)
    producer_paths=[Path('biosynvia')/name for name in ['stage12.py','preparation.py','source.py','__init__.py']]+[Path('scripts/build_stage12.py'),Path('docs/stage12-executable-spec.md')]
    consumed.update({str(path):fingerprint(path) for path in producer_paths})
    assays=pd.read_csv(parent/'original_offline.csv',float_precision='round_trip')
    aligned=pd.read_csv(parent/'combined_inline.csv',usecols=['run_id','Time (h)'],float_precision='round_trip') if (parent/'combined_inline.csv').exists() else None
    aligned_bounds=aligned.groupby('run_id')['Time (h)'].agg(['min','max']) if aligned is not None else None
    stage.mkdir(parents=True)
    for path in producer_paths:
        dest=stage/'producer'/path
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,dest)
    for name in CONTRACTS:
        shutil.copyfile(config_directory/f'{name}.json',stage/f'{name}.json')
    lineage=[]; raw_assays=[]; cadence=[]; collisions=[]; dictionary=[]; timing=[]
    with zipfile.ZipFile(backup) as z:
        for item in source['files']:
            if not item['path'].endswith('.xlsx'): continue
            raw=z.read(item['path']); member_hash=sha256(raw).hexdigest()
            wb=openpyxl.load_workbook(io.BytesIO(raw),read_only=True,data_only=False)
            for sheet in wb:
                frame,headers=read_sheet(sheet)
                reactor=sheet.title.split('_')[0]; run=f'{item["experiment_id"]}_{reactor}'
                ref={'experiment_id':item['experiment_id'],'reactor_id':reactor,'run_id':run,'process_mode':item['process_mode'],
                     'source_file':item['path'],'source_sha256':member_hash,'source_sheet':sheet.title}
                selected=assays[assays.run_id.eq(run)]
                for field in headers:
                    if field in ('Time (h)','Status'):continue
                    qualifier=field[field.find('(')+1:field.rfind(')')] if '(' in field else ''
                    is_frequency=field.startswith('C (')
                    dictionary.append({**ref,'field':field,'feature':feature_id(field) if '_offline_' not in sheet.title else 'offline__'+feature_id(field)[3:],
                        'modality':'offline' if '_offline_' in sheet.title else 'sensor','unit_header':None if is_frequency or field.startswith('Fitting ') else qualifier or None,
                        'frequency_qualifier':qualifier if is_frequency else None,'unit_status':'unverified_header_only',
                        'has_status_column':'Status' in headers,'family':sheet.title.split('_',2)[-1],
                        'proposal':'forbidden_offline_input' if '_offline_' in sheet.title else 'five_core_feasibility' if field in FIVE else 'blocked_unknown_status' if 'Status' not in headers else 'semantic_review_required',
                        'input_approved':False})
                if '_offline_' in sheet.title:
                    for _,row in frame.iterrows():
                        matches=selected[pd.to_numeric(selected['Time (h)']).eq(row['Time (h)'])]
                        if len(matches)!=1:raise ValueError('Original assay key mismatch')
                        assay_id=matches.assay_id.iloc[0]
                        for column,field in enumerate(headers,1):
                            value=row[field]; numeric=pd.to_numeric(pd.Series([value]),errors='coerce').iloc[0]
                            raw_assays.append({**ref,'assay_id':assay_id,'field':field,'source_cell':f'{get_column_letter(column)}{int(row["_excel_row"])}',
                                'source_cell_type':row['_cell_types'][field], 'raw_value_json':json_dumps(None if pd.isna(value) else value),
                                'value':float(numeric) if pd.notna(numeric) and np.isfinite(numeric) else None,'source_blank':bool(pd.isna(value)), 'predictor_allowed':False})
                    continue
                times=pd.to_numeric(frame['Time (h)'],errors='coerce'); finite=times[np.isfinite(times)]
                delta=np.diff(np.sort(finite.unique())); positive=delta[delta>0]
                duplicate=times.notna() & np.isfinite(times) & times.duplicated(keep=False)
                cadence.append({**ref,'rows':len(frame),'invalid_times':int((~np.isfinite(times)).sum()),'duplicate_rows':int(duplicate.sum()),
                    'backward_steps':int((np.diff(finite)<0).sum()),'first_hours':float(finite.min()),'last_hours':float(finite.max()),
                    'median_cadence_seconds':float(np.median(positive)*3600),'p95_cadence_seconds':float(np.quantile(positive,.95)*3600),'max_gap_hours':float(positive.max()),
                    'has_status_column':'Status' in headers,'status_counts_json':json_dumps(dict(Counter('<blank>' if pd.isna(v) else str(v) for v in frame.Status)),sort_keys=True) if 'Status' in headers else '{}'})
                timing.append({**ref,'event_time_header':'Time (h)','time_origin':'unknown elapsed-time origin','raw_to_aligned_transform':'unresolved; no export/resampling algorithm recovered',
                    'raw_feature_policy':'latest prior per raw stream; no aligned-value predictor','offset_status':'unknown','tolerance_status':'unapproved',
                    'raw_first_hours':float(finite.min()),'raw_last_hours':float(finite.max()),
                    'aligned_first_hours':float(aligned_bounds.loc[run,'min']) if aligned_bounds is not None else None,
                    'aligned_last_hours':float(aligned_bounds.loc[run,'max']) if aligned_bounds is not None else None,
                    'raw_minus_aligned_end_hours':float(finite.max()-aligned_bounds.loc[run,'max']) if aligned_bounds is not None else None,
                    'mismatch_acceptance':'not_assessed_no_approved_tolerance','aligned_source_file':next(i['path'] for i in source['files'] if i.get('experiment_id')==item['experiment_id'] and i.get('reactor_id')==reactor and i.get('measurement_kind')=='inline')})
                for _,row in frame[duplicate].iterrows():
                    collisions.append({**ref,'time_hours':float(row['Time (h)']),'source_excel_row':int(row['_excel_row']),
                        'raw_row_json':json_dumps({h:None if pd.isna(row[h]) else row[h] for h in headers},sort_keys=True)})
                for assay in selected.itertuples(index=False):
                    cutoff=float(selected.loc[selected.assay_id.eq(assay.assay_id),'Time (h)'].iloc[0])
                    for row in snapshot_flags(frame,headers,cutoff):
                        lineage.append({**ref,'assay_id':assay.assay_id,**row})
            wb.close()
            print(f'Protocol evidence: {item["experiment_id"]}',flush=True)
    line=pd.DataFrame(lineage); origins=pd.DataFrame(raw_assays)
    if len(line)!=len(assays)*40 or line.duplicated(['assay_id','feature']).any():raise ValueError('Incomplete/duplicate feature lineage')
    decisions=assays.copy()
    original_values=origins.drop_duplicates(['assay_id','field']).pivot(index='assay_id',columns='field',values='value')
    for field in original_values:
        if field in decisions:
            decisions[field]=decisions.assay_id.map(original_values[field])
    assert_original_assays(decisions,origins)
    decisions['positive_only_proposal']=pd.to_numeric(decisions[TARGET]).gt(0)
    decisions['recorded_nonnegative_proposal']=pd.to_numeric(decisions[TARGET]).ge(0)
    decisions['target_availability_hours']=None
    decisions['assay_quality_status']='unknown'
    for label,fields,strict in [('five',FIVE,False),('eight',CORE_FIELDS,False),('strict_availability_five',FIVE,True)]:
        selected=line[line.field.isin(fields)].copy()
        good=selected.strict_availability_eligible if strict else selected.assumed_acquisition_eligible
        complete=good.groupby(selected.assay_id).sum().eq(len(fields))
        decisions[f'{label}_complete']=decisions.assay_id.map(complete).fillna(False)
    old=pd.read_csv(parent/'processed_candidates.csv').set_index('assay_id')
    decisions['v3_eight_assumed_status_complete']=decisions.assay_id.map(old.core_features_complete)
    coverage=decisions.groupby(['experiment_id','reactor_id','process_mode'],as_index=False).agg(assays=('assay_id','size'),five_complete=('five_complete','sum'),eight_complete=('eight_complete','sum'),strict_availability_five_complete=('strict_availability_five_complete','sum'),v3_eight_complete=('v3_eight_assumed_status_complete','sum'),positive_targets=('positive_only_proposal','sum'),recorded_nonnegative_targets=('recorded_nonnegative_proposal','sum'))
    split=proposed_split(coverage)
    write_json(stage/'split_manifest.json',split)
    effects=[]
    for age in [1,5,15]:
        # The only age-dependent flag is recomputed; all other prefix evidence stays fixed.
        eligible=~line[[c for c in ['no_past_observation','duplicate_source_time','invalid_value','status_column_absent','status_value_blank','status_not_ok','past_only_derived_zero']]].any(axis=1) & line.age_hours.le(age/60+TOL)
        for family,fields in [('five',FIVE),('eight',CORE_FIELDS)]:
            subset=line.field.isin(fields)
            complete=eligible[subset].groupby(line.loc[subset,'assay_id']).sum().eq(len(fields))
            for key,group in decisions.groupby(['experiment_id','reactor_id','process_mode']):
                support=group.assay_id.map(complete).fillna(False)
                effects.append(dict(zip(['experiment_id','reactor_id','process_mode'],key),family=family,age_minutes=age,assays=len(group),supported=int(support.sum()),positive_supported=int((support & group.positive_only_proposal).sum()),nonnegative_supported=int((support & group.recorded_nonnegative_proposal).sum()),strict_availability_supported=0))
    target_coverage=[]
    for key,group in decisions.groupby(['experiment_id','reactor_id','process_mode']):
        delta=np.diff(np.sort(group['Time (h)'].unique()))
        target_coverage.append(dict(zip(['experiment_id','reactor_id','process_mode'],key),assays=len(group),positive=int(group.positive_only_proposal.sum()),numeric_zero=int(group[TARGET].eq(0).sum()),median_assay_interval_hours=float(np.median(delta)),min_assay_interval_hours=float(min(delta)),max_assay_interval_hours=float(max(delta))))
    eligibility=pd.DataFrame(dictionary)
    schema_columns=['source_path','source_kind','run_id','schema_role','column_count','headers_json','sheet_count']
    tables={'assay_decisions':decisions,'feature_lineage':line,'assay_source_cells':origins,'field_dictionary':eligibility,'feature_eligibility':eligibility[eligibility.modality.eq('sensor')].drop_duplicates(['feature','source_file','source_sheet']), 'stream_cadence':pd.DataFrame(cadence),'source_collisions':pd.DataFrame(collisions,columns=['experiment_id','reactor_id','run_id','process_mode','source_file','source_sha256','source_sheet','time_hours','source_excel_row','raw_row_json']),'time_policy':pd.DataFrame(timing),'group_coverage':coverage,'sample_effects':pd.DataFrame(effects),'target_coverage':pd.DataFrame(target_coverage),'source_schema_inventory':pd.DataFrame(source_schema,columns=schema_columns)}
    with sqlite3.connect(stage/'biosynvia.sqlite') as connection:
        for name,frame in tables.items():
            frame.to_csv(stage/f'{name}.csv',index=False,float_format='%.17g')
            frame.to_sql(name,connection,index=False,if_exists='fail')
        connection.execute('CREATE UNIQUE INDEX lineage_key ON feature_lineage(assay_id,feature)')
        connection.execute('CREATE UNIQUE INDEX assay_key ON assay_decisions(assay_id)')
    # Every consumed mutable file and source copy is rechecked before promotion.
    for name,digest in consumed.items():
        if fingerprint(name)!=digest:raise ValueError(f'Input changed during run: {name}')
    if fingerprint(archive)!=source['sha256'] or fingerprint(backup)!=source['sha256']:raise ValueError('Source/backup changed')
    manifest={'schema_version':'1.0','status':'complete_protocol_artifacts_not_scientifically_approved','created_at_utc':datetime.now(timezone.utc).isoformat(),
        'source_sha256':source['sha256'],'source_md5':source['md5'],'backup_path':str(backup),'backup_sha256':fingerprint(backup),'consumed_inputs':consumed,
        'command':command or ' '.join(sys.argv),'working_directory':str(Path.cwd()),'environment':{'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__,'openpyxl':openpyxl.__version__,'sqlite':sqlite3.sqlite_version},
        'tables':{name:len(frame) for name,frame in tables.items()},'target_approved':False,'split_approved':False,'features_approved':False,'model_fit_permitted':False,
        'stable_reproduction':'CSV/config/producer/split payloads byte-identical in pinned environment; SQLite compared logically; manifest time/command/paths may vary',
        'source_rights':'unresolved; no redistribution','retrieved_at_utc':None,'prior_global_eda_disclosed':True,
        'outputs':{str(path.relative_to(stage)):fingerprint(path) for path in sorted(stage.rglob('*')) if path.is_file()}}
    write_json(stage/'stage12_manifest.json',manifest)
    verify_bundle(stage)
    stage.rename(output)
    return manifest
