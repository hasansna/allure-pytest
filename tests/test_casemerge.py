"""
Test parameter --allure_casemerge.
- test if passed test cases are merged if total count of tests exceeds provided parameter value
- test if test cases are not merged if total count of tests doeesn't exceed parameter value
- test if merged tests remain their steps, status and attachments
Created on Aug 30, 2017
@author: hasansna
"""


import pytest

def test_smoke(report_for):

    extra_run_args = list()

    extra_run_args.extend(['--allure_casemerge', '4'])

    report = report_for("""
    import pytest
    import allure
    @pytest.mark.parametrize("fake_input",  range(1, 11))
    def test_passed(fake_input):
    with allure.step("Step #1" % fake_input):
        with allure.step("Step #2"):
            assert 1==1
    """ , extra_run_args=extra_run_args)

    assert len(report.find('.//test-case')) == 3
