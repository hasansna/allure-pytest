"""
Test parameter --allure_optimizereport.
- test if attachment gets removed from passed testcases
- test if label gets removed from passed testcases
- test if steps removed from passed test cases

Created on Aug 30, 2017

@author: hasansna
"""


import pytest


from hamcrest import assert_that, is_not, has_property, contains, has_entries, \
    has_properties, has_item, anything, all_of, any_of,equal_to
from allure.constants import AttachmentType
from allure.utils import all_of

import pprint

def test_smoke(report_for):

    extra_run_args = list()
    extra_run_args.extend(['--allure_stories', 'attachments,steps,labels'])

    report = report_for("""
    import pytest
    import allure

    def test_x():
        %s.attach('Foo', 'Bar')
    """ % extra_run_args)

    print "Report!!!"
    pprint.pprint(report)

    assert_that(is_not(report.findall('test-cases/test-case/attachments/attachment'),
                contains(has_property('attrib', has_entries(title='Foo')))))
