"""
Test parameter --allure_optimizereport.
- test if attachment gets removed from passed testcases
- test if label gets removed from passed testcases
- test if steps removed from passed test cases

Created on Aug 30, 2017

@author: hasansna
"""


import pytest

def xml_test(report):
    if report.find('.//attachment') != None:
        print "attachment found in report"
        assert False
    if report.find('.//label') != None:
        print "Label found in report"
        assert False
    if report.find('.//step') != None:
        print "step found in report"
        assert False

def test_smoke(report_for):

    extra_run_args = list()

    extra_run_args.extend(['--allure_optimizereport', 'attachments,steps,labels'])

    report = report_for("""
    import pytest
    import allure

    def test():
        with pytest.allure.step(title='step_1'):
            assert True
        pytest.allure.attach('Foo', 'Bar')
    """ , extra_run_args=extra_run_args)

    xml_test(report)


