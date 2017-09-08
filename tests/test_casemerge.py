"""
Test parameter --allure_casemerge.
- test if passed test cases are merged if total count of tests exceeds provided parameter value
- test if test cases are not merged if total count of tests doeesn't exceed parameter value
- test if merged tests remain their steps, status and attachments
Created on Sep 8, 2017
@author: TietoLV
"""


import pytest

def test_smoke(report_for):

    extra_run_args = list()

    extra_run_args.extend(['--allure_casemerge=2'])

    report = report_for("""
    import pytest
    import allure
    @pytest.mark.parametrize("input", [1,2,3])
    def test_passed(input):
        assert 1==1
    """ , extra_run_args=extra_run_args)

    assert len(report.findall('test-cases/test-case')) == 2
    assert report.find('name').text.endswith('_(MERGED)')
    for case_name in ['range_from_1_to_2', 'range_from_3_to_3']:
        xpath=".//a[text()=\"%s\"]" % case_name
        assert report.xpath(xpath) is not None

def test_failed_cases_are_not_touched(report_for):

    extra_run_args = list()

    extra_run_args.extend(['--allure_casemerge=2'])

    report = report_for("""
    import pytest
    import allure
    @pytest.mark.parametrize("input", [1,2,3])
    def test_passed(input):
        assert 1==1

    @pytest.mark.parametrize("input", [1,2])
    def test_failed(input):
        assert 1!=1
    """ , extra_run_args=extra_run_args)

    assert len(report.findall('test-cases/test-case')) == 4
    assert report.find('name').text.endswith('_(MERGED)')
    for case_name in ['range_from_1_to_2', 'range_from_3_to_3', 'test_failed[1]', 'test_failed[2]']:
        xpath=".//a[text()=\"%s\"]" % case_name
        assert report.xpath(xpath) is not None

def test_casemerge_is_less_than_total_case_count(report_for):
    extra_run_args = list()

    extra_run_args.extend(['--allure_casemerge=3'])

    report = report_for("""
    import pytest
    import allure
    @pytest.mark.parametrize("input", [1,2])
    def test_passed(input):
        assert 1==1
    """ , extra_run_args=extra_run_args)

    assert len(report.findall('test-cases/test-case')) == 2
    assert not report.find('name').text.endswith('_(MERGED)')

def test_casemerge_equals_total_case_count(report_for):
    extra_run_args = list()

    extra_run_args.extend(['--allure_casemerge=3'])

    report = report_for("""
    import pytest
    import allure
    @pytest.mark.parametrize("input", [1,2,3])
    def test_passed(input):
        assert 1==1
    """ , extra_run_args=extra_run_args)

    assert len(report.findall('test-cases/test-case')) == 3
    assert not report.find('name').text.endswith('_(MERGED)')

def test_if_substeps_are_correct(report_for):
    _run_args = list()

    extra_run_args.extend(['--allure_casemerge=2'])

    report = report_for("""
    import pytest
    import allure
    @pytest.mark.parametrize("input", [1,2,3])
    def test_passed(input):
        with allure("Step1"):
            with allure("Step2"):
                assert 1==1
    """ , extra_run_args=extra_run_args)

    assert report.xpath('.//a[text()="test_passed[1]"]').getparent().find('steps/step/title').text == 'Step1'
    assert report.xpath('.//a[text()="test_passed[1]"]').getparent().find('steps/steps/steps/title').text == 'Step2'

def test_if_attachments_are_correct(report_for):
    _run_args = list()

    extra_run_args.extend(['--allure_casemerge=2'])

    report = report_for("""
    import pytest
    import allure
    @pytest.mark.parametrize("input", [1,2,3])
    def test_passed(input):
        allure.attach('Attachment', 'Some text')
        assert 1==1
    """ , extra_run_args=extra_run_args)

    assert report.xpath('.//a[text()="test_passed[1]"]').getparent().find('attachments/attachment').attrib['title'] == 'Attachment'
