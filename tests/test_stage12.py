import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
import openpyxl
import pandas as pd
from biosynvia.stage12 import (ALIGNED_INLINE_HEADERS, ALIGNED_OFFLINE_HEADERS, EXPECTED_SHEETS,
                               assert_source_schema, cutoff_mask, read_sheet, snapshot_flags,
                               proposed_split, verify_bundle)

class Stage12Tests(unittest.TestCase):
    def frame(self):
        return pd.DataFrame({'Time (h)':[0.,1.,2.],'C (300kHz)':[0.,0.,7.],'Status':['Ok','Warning Active','Ok'],'_excel_row':[2,4,5]})

    def test_availability_delayed_unknown_future_and_exact_tie(self):
        np.testing.assert_array_equal(cutoff_mask([0,1,2,1],[0,1.5,1,np.nan],1),[True,False,False,False])
        np.testing.assert_array_equal(cutoff_mask([0,1,2,1],[0,1.5,1,np.nan],1,True),[True,True,False,True])

    def test_independent_flags_and_future_prefix_invariance(self):
        frame=self.frame(); headers=['Time (h)','C (300kHz)','Status']
        original=snapshot_flags(frame,headers,1.2)[0]
        self.assertTrue(original['stale']); self.assertTrue(original['status_not_ok']); self.assertTrue(original['past_only_derived_zero'])
        frame.loc[2,['C (300kHz)','Status']]=[999,'Bad']
        self.assertEqual(original,snapshot_flags(frame,headers,1.2)[0])
        self.assertEqual(original['source_cell'],'B4')
        self.assertIsNone(original['proposed_value'])

    def test_unknown_and_blank_status_not_silently_ok(self):
        frame=self.frame(); no=frame.drop(columns='Status')
        row=snapshot_flags(no,['Time (h)','C (300kHz)'],2)[0]
        self.assertTrue(row['status_column_absent']); self.assertFalse(row['assumed_acquisition_eligible'])
        frame.loc[2,'Status']=None
        row=snapshot_flags(frame,['Time (h)','C (300kHz)','Status'],2)[0]
        self.assertTrue(row['status_value_blank']);self.assertFalse(row['status_column_absent'])

    def test_internal_blank_excel_row_coordinates(self):
        wb=openpyxl.Workbook(); ws=wb.active
        ws.append(['Time (h)','signal','Status']);ws.append([0,1,'Ok']);ws.append([None,None,None]);ws.append([1,2,'Ok'])
        frame,headers=read_sheet(ws)
        row=snapshot_flags(frame,headers,1)[0]
        self.assertEqual(row['source_cell'],'B4');self.assertEqual(row['source_time_cell'],'A4');self.assertEqual(row['source_status_cell'],'C4')

    def test_duplicate_identical_and_conflicting_preserved(self):
        for values in ([1,1],[1,2]):
            frame=pd.DataFrame({'Time (h)':[0,0],'signal':values,'Status':['Ok','Ok'],'_excel_row':[2,3]})
            row=snapshot_flags(frame,['Time (h)','signal','Status'],0)[0]
            self.assertTrue(row['duplicate_source_time']);self.assertIsNone(row['proposed_value']);self.assertIsNone(row['source_cell'])
            self.assertEqual([c['raw_value'] for c in json.loads(row['source_candidates_json'])],values)

    def test_invalid_prefix_does_not_claim_all_finite_zero(self):
        frame=pd.DataFrame({'Time (h)':[0,1],'C (300kHz)':[np.nan,0],'Status':['Ok','Ok'],'_excel_row':[2,3]})
        self.assertFalse(snapshot_flags(frame,['Time (h)','C (300kHz)','Status'],1)[0]['past_only_derived_zero'])

    def coverage(self):
        return pd.DataFrame([{'experiment_id':f'EXP{i:03}','reactor_id':r,'process_mode':'batch' if i<4 else 'fed-batch','assays':10,'five_complete':8 if i in [2,4] else 7,'target':i} for i in range(1,7) for r in ['R01','R02']])

    def test_split_target_blind_permutation_exact_winners_and_group_folds(self):
        coverage=self.coverage();split=proposed_split(coverage)
        self.assertEqual(split['test_groups'],['EXP002','EXP004'])
        coverage['target']=None
        self.assertEqual(split,proposed_split(coverage.sample(frac=1,random_state=4)))
        tests=set(split['test_groups'])
        for fold in split['outer_development_folds']:
            self.assertFalse(set(fold['train']) & set(fold['validation']));self.assertFalse(tests & set(fold['train']))
            for inner in fold['inner_folds']:
                self.assertFalse(set(inner['train']) & set(inner['validation']));self.assertTrue(set(inner['train']+inner['validation'])<=set(fold['train']))

    def test_split_rejects_duplicate_and_missing_pair_and_exact_tie(self):
        coverage=self.coverage()
        with self.assertRaises(ValueError):proposed_split(pd.concat([coverage,coverage.iloc[:1]]))
        with self.assertRaises(ValueError):proposed_split(coverage.iloc[1:])
        coverage['five_complete']=7
        self.assertEqual(proposed_split(coverage)['test_groups'],['EXP001','EXP004'])

    def test_existing_output_and_incomplete_protected_before_read(self):
        from biosynvia.stage12 import build
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'v4';output.mkdir()
            with self.assertRaisesRegex(ValueError,'preserved'):build('absent','absent',output)
            output.rmdir();output.with_name('v4.incomplete').mkdir()
            with self.assertRaisesRegex(ValueError,'preserved'):build('absent','absent',output)

    def test_exact_publisher_schema_rejects_wrong_sheet_and_csv_headers(self):
        import io, shutil, zipfile
        with tempfile.TemporaryDirectory() as directory:
            archive=Path(directory)/'source.zip'; files=[]
            with zipfile.ZipFile(archive, 'w') as z:
                for number in range(1,13):
                    experiment=f'EXP{number:03}'; mode='batch' if number < 10 else 'fed-batch'
                    workbook=openpyxl.Workbook(); workbook.remove(workbook.active)
                    for sheet in sorted(EXPECTED_SHEETS): workbook.create_sheet(sheet)
                    stream=io.BytesIO(); workbook.save(stream)
                    name=f'{experiment}_{mode}.xlsx'; z.writestr(name,stream.getvalue())
                    files.append({'path':name,'experiment_id':experiment,'process_mode':mode,'measurement_kind':'workbook'})
                    for reactor in ('R01','R02'):
                        for kind,header in [('inline',ALIGNED_INLINE_HEADERS),('offline',ALIGNED_OFFLINE_HEADERS)]:
                            name=f'{experiment}_{mode}_{reactor}_{kind}.csv'; z.writestr(name, ','.join(header)+'\n')
                            files.append({'path':name,'experiment_id':experiment,'reactor_id':reactor,'process_mode':mode,'measurement_kind':kind})
            assert_source_schema(archive, {'files':files})
            bad_archive=Path(directory)/'bad-source.zip'; shutil.copyfile(archive,bad_archive)
            workbook=openpyxl.Workbook(); workbook.remove(workbook.active)
            for sheet in sorted(EXPECTED_SHEETS - {'R01_inline_CO2'}): workbook.create_sheet(sheet)
            workbook.create_sheet('R01_unexpected')
            stream=io.BytesIO(); workbook.save(stream)
            with zipfile.ZipFile(bad_archive, 'a') as z: z.writestr('EXP001_batch.xlsx',stream.getvalue())
            with self.assertRaisesRegex(ValueError, 'Workbook sheet schema mismatch'):
                assert_source_schema(bad_archive, {'files':files})
            with zipfile.ZipFile(archive, 'a') as z: z.writestr('EXP001_batch_R01_inline.csv', 'wrong\n')
            with self.assertRaisesRegex(ValueError, 'Aligned CSV schema mismatch'):
                assert_source_schema(archive, {'files':files})

    def test_bundle_tamper_missing_file_and_logical_csv_sql_mismatch(self):
        from biosynvia.preparation import fingerprint
        import sqlite3
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory);frame=pd.DataFrame({'value':[0.,None]})
            frame.to_csv(output/'fixture.csv',index=False)
            with sqlite3.connect(output/'biosynvia.sqlite') as c:frame.to_sql('fixture',c,index=False)
            outputs={p.name:fingerprint(p) for p in output.iterdir()}
            manifest={'outputs':outputs,'tables':{'fixture':2}}
            (output/'stage12_manifest.json').write_text(json.dumps(manifest))
            verify_bundle(output)
            (output/'fixture.csv').write_text('value\n9\n')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):verify_bundle(output)
            manifest['outputs']['fixture.csv']=fingerprint(output/'fixture.csv');(output/'stage12_manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(AssertionError):verify_bundle(output)
            (output/'fixture.csv').unlink()
            with self.assertRaisesRegex(ValueError,'hash mismatch'):verify_bundle(output)

class Stage12IntegrationTests(unittest.TestCase):
    def fixture(self, root):
        from biosynvia.preparation import CORE_FIELDS, TARGET, fingerprint
        import io, zipfile
        archive=root/'source.zip';parent=root/'parent';parent.mkdir();rows=[];files=[]
        with zipfile.ZipFile(archive,'w') as z:
            for number in range(1,7):
                exp=f'EXP{number:03}';mode='batch' if number<4 else 'fed-batch';member=f'{exp}_{mode}.xlsx'
                wb=openpyxl.Workbook();wb.remove(wb.active)
                for reactor in ['R01','R02']:
                    cell=wb.create_sheet(f'{reactor}_offline_CellAnalysis');cell.append(['Time (h)',TARGET]);cell.append([0,0]);cell.append([1,99466.66666666667])
                    medium=wb.create_sheet(f'{reactor}_offline_MediumAnalysis');medium.append(['Time (h)','Glucose (g/L)']);medium.append([1,None]);medium.append([0,3])
                    sensor=wb.create_sheet(f'{reactor}_inline_Test')
                    sensor.append(['Time (h)',*CORE_FIELDS,*[f'other{i}' for i in range(32)],'Status'])
                    sensor.append([0,*([1]*40),'Ok']);sensor.append([1,*([2]*40),'Ok'])
                    for i,t in enumerate([0.,1.]):rows.append({'assay_id':f'{exp}_{reactor}_{i}','run_id':f'{exp}_{reactor}','experiment_id':exp,'reactor_id':reactor,'process_mode':mode,'Time (h)':t,TARGET:0. if i==0 else 99466.66666666667,'Glucose (g/L)':3. if i==0 else None,'scientific_label_approved':False})
                    files.append({'path':f'{exp}_{reactor}_inline.csv','experiment_id':exp,'reactor_id':reactor,'measurement_kind':'inline'})
                handle=io.BytesIO();wb.save(handle);z.writestr(member,handle.getvalue());files.append({'path':member,'experiment_id':exp,'process_mode':mode})
        digest=fingerprint(archive);backup=root/'backup.zip';backup.write_bytes(archive.read_bytes())
        pd.DataFrame(rows).to_csv(parent/'original_offline.csv',index=False)
        pd.DataFrame({'assay_id':[r['assay_id'] for r in rows],'core_features_complete':True}).to_csv(parent/'processed_candidates.csv',index=False)
        outputs={p.name:{'sha256':fingerprint(p)} for p in parent.iterdir()}
        (parent/'preparation_manifest.json').write_text(json.dumps({'source_sha256':digest,'backup_path':str(backup),'outputs':outputs}))
        return archive,parent,{'sha256':digest,'md5':'synthetic-fixture','files':files}

    def test_full_build_reproduction_zero_null_coordinates_and_failure_gate(self):
        from biosynvia.stage12 import build, verify_bundle
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);archive,parent,source=self.fixture(root)
            with patch('biosynvia.stage12.inventory_archive',return_value=source), patch('biosynvia.stage12.assert_source_schema',return_value=[]):
                first=build(archive,parent,root/'one');second=build(archive,parent,root/'two')
                for name,digest in first['outputs'].items():
                    if name!='biosynvia.sqlite':self.assertEqual(digest,second['outputs'][name],name)
                verify_bundle(root/'one')
                actual=pd.read_csv(root/'one'/'assay_decisions.csv',float_precision='round_trip')
                lineage=pd.read_csv(root/'one'/'feature_lineage.csv',float_precision='round_trip')
                assay_keys=actual.set_index('assay_id')[['experiment_id','reactor_id','run_id']]
                matched=lineage.join(assay_keys, on='assay_id', rsuffix='_assay')
                self.assertTrue(matched.run_id.eq(matched.run_id_assay).all())
                self.assertTrue(matched.experiment_id.eq(matched.experiment_id_assay).all())
                self.assertTrue(matched.reactor_id.eq(matched.reactor_id_assay).all())
                self.assertTrue(actual[actual['Time (h)'].eq(1)]['VCD Mean (cells/mL)'].eq(99466.66666666667).all())
                cells=pd.read_csv(root/'one'/'assay_source_cells.csv')
                self.assertEqual(cells[cells.field.eq('VCD Mean (cells/mL)')].value.eq(0).sum(),12)
                self.assertEqual(cells[cells.field.eq('Glucose (g/L)')].source_blank.sum(),12)
                self.assertTrue(cells[cells.field.eq('VCD Mean (cells/mL)') & cells.value.eq(0)].source_cell.eq('B2').all())
                with patch('biosynvia.stage12.verify_bundle',side_effect=ValueError('injected validation failure')):
                    with self.assertRaisesRegex(ValueError,'injected'):build(archive,parent,root/'failed')
                self.assertFalse((root/'failed').exists());self.assertTrue((root/'failed.incomplete').exists())
                # All consumed parent bytes are checked before any output is started.
                with (parent/'original_offline.csv').open('a') as handle:handle.write('\n')
                with self.assertRaisesRegex(ValueError,'Parent artifact hash mismatch'):build(archive,parent,root/'tampered')
                self.assertFalse((root/'tampered').exists());self.assertFalse((root/'tampered.incomplete').exists())
