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
    def test_passed1():
        assert 1==1

    def test_passed2():
        assert 1==1

    def test_passed3():
        assert 1==1
    """ , extra_run_args=extra_run_args)

    assert len(report.findall('test-cases/test-case')) == 2
    for test_case in report.findall('test-cases/test-case'):
        assert test_case.find('name').text.endswith('_(MERGED)')
