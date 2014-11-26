#!/user/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 2013.7.12

@author: xing, peng.jin
'''
import re

try:
    import Image
except:
    from PIL import Image


import os
from lxml import etree
from StringIO import StringIO
import string

from result import Result
import htmlparser as htmlparser
import headerchecker as headerchecker
from httpclient_obj import httpclient
import env as ENV


class SinglePageChecker(Result):
    '''
    checker only change case's result message , will never change case's result
    '''

    def __init__(self, case, page=None):
        super(SinglePageChecker, self).__init__()
        self._case = case
        self._name = "BaseChecker"
        self._page = None

    def set_page(self, page):
        self._page = page

    def is_ok(self, page=None):
        return True

    def get_name(self):
        return self._name


    def set_result_message(self, message):
        super(SinglePageChecker, self).set_result_message(message)
        self._case.debug_message(message)


class PageNotNullChecker(SinglePageChecker):
    def __init__(self, case):
        super(PageNotNullChecker, self).__init__(case)
        self._name = "PageNotNullChecker"

    def is_ok(self, page=None):
        if page:
            self._page = page
        if self._page.content and self._page.content != "":
            self.set_result_message("checker name %s content is not null" % self._name)
            self.set_result(True)
        else:
            self.set_result_message("checker name %s content is null" % self._name)
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class ResponseCodeChecker(SinglePageChecker):
    def __init__(self, expected_code=200, expected_eq=True, case=None):
        super(ResponseCodeChecker, self).__init__(case)
        self._name = "ResponseCodeChecker"
        self._expected_code = expected_code
        self._expected_eq = expected_eq

    def is_ok(self, page=None):

        actually_reposne_code = page.status_code

        self.set_result_message("checker name %s ; expected response code :%s  actually : %s, expected_eq %s" % (
            self._name, self._expected_code, actually_reposne_code, self._expected_eq))

        actually_eq = (actually_reposne_code == self._expected_code)
        if self._expected_eq and actually_eq:
            self.set_result(True)
        elif (not self._expected_eq) and (not actually_eq):
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class JsCountChecker(SinglePageChecker):
    def __init__(self, expected_js, case):
        super(JsCountChecker, self).__init__(case)
        self._name = "JsCountChecker"
        self._expected_js = expected_js

    def is_ok(self, page):
        all_js = htmlparser.get_all_js(page)
        len_all_js = len(all_js)
        self.set_result_message(
            "checker name %s expected js count is %s , actually %s" % (self._name, self._expected_js, len_all_js))

        if len_all_js == self._expected_js:
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class CssCountChecker(SinglePageChecker):
    def __init__(self, expected_css, case):
        super(CssCountChecker, self).__init__(case)
        self._name = "CssCountChecker"
        self._expected_css = expected_css

    def is_ok(self, page):
        all_css = htmlparser.get_all_css(page)
        len_all_css = len(all_css)
        self.set_result_message(
            "checker name %s expected css count is %s , actually %s" % (self._name, self._expected_css, len_all_css))

        if len_all_css == self._expected_css:
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class AllAssetCountChecker(SinglePageChecker):
    def __init__(self, expected_all_asset, case):
        super(AllAssetCountChecker, self).__init__(case)
        self._name = "AllAssetCountChecker"
        self._expected_all_asset = expected_all_asset

    def is_ok(self, page):
        all_link = htmlparser.get_all_links(page)
        len_all_link = len(all_link)
        self.set_result_message("checker name %s expected asset count is %s , actually %s" % (
            self._name, self._expected_all_asset, len_all_link))

        if len_all_link == self._expected_all_asset:
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class DataUriCountChecker(SinglePageChecker):
    def __init__(self, expected_datauri_img, expected_datauri_css, case):
        super(DataUriCountChecker, self).__init__(case)
        self._name = "DataUriCountChecker"
        self._expected_datauri_img = expected_datauri_img
        self._expected_datauri_css = expected_datauri_css

    def is_ok(self, page):
        HTML_CONTENT_TYPE = 'text/html'
        CSS_CONTENT_TYPE = 'text/css'

        res_headers = page.res_headers
        content_type = headerchecker.get_content_type(res_headers)

        if HTML_CONTENT_TYPE in content_type:
            all_datauri_img = htmlparser.get_datauri_img(page)
            all_datauri_css = htmlparser.get_datauri_css(page)
            if all_datauri_img != None:
                len_all_datauri_img = len(all_datauri_img)
            else:
                len_all_datauri_img = 0
            if all_datauri_css != None:
                len_all_datauri_css = len(all_datauri_css)
            else:
                len_all_datauri_css = 0
        elif CSS_CONTENT_TYPE in content_type:
            # there is bugs for parser css ,so we choose trick method to check the datauir numbers
            len_all_datauri_img = page.content.count("data:image/")
            len_all_datauri_css = page.content.count("Y$DU.css?")

        result_message = "checker name %s expected datauri img count is %s , actually %s" % (
            self._name, self._expected_datauri_img, len_all_datauri_img, )
        result_message += ", expected datauri css count is %s , actually %s" % (
            self._expected_datauri_css, len_all_datauri_css)

        # result_message += ", all page content is %s" % (page.content)
        self.set_result_message(result_message)

        if len_all_datauri_img == self._expected_datauri_img and len_all_datauri_css == self._expected_datauri_css:
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class DistributedCacheChecker(SinglePageChecker):
    def __init__(self, expected_cache, case):
        super(DistributedCacheChecker, self).__init__(case)
        self._name = "DistributedCacheChecker"
        self._expected_cache = expected_cache

    def is_ok(self, page):
        result_message = "checker name %s expected %s hit DistributedCache , actually %s" % ( self._name, "%s", "%s")
        if self._expected_cache:
            if headerchecker.check_feature(page.res_headers, headerchecker.DISTRIBUTE_CACHE, True):
                self.set_result_message(result_message % ("", "DistributedCache"))
                self.set_result(True)
            else:
                self.set_result_message(result_message % ("", "Not DistributedCache"))
                self.set_result(False)
        else:
            if headerchecker.check_feature(page.res_headers, headerchecker.TPU_CACHE, True):
                self.set_result_message(result_message % ("not", "DistributedCache"))
                self.set_result(False)
            else:
                self.set_result_message(result_message % ("not", "Not DistributedCache"))
                self.set_result(True)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class CacheChecker(SinglePageChecker):
    def __init__(self, expected_cache, case):
        super(CacheChecker, self).__init__(case)
        self._name = "CacheChecker"
        self._expected_cache = expected_cache

    def is_ok(self, page):
        result_message = "checker name %s expected %s hit cache , actually %s" % ( self._name, "%s", "%s")
        if self._expected_cache:
            if headerchecker.check_feature(page.res_headers, headerchecker.TPU_CACHE, True):
                self.set_result_message(result_message % ("", "Cache"))
                self.set_result(True)
            else:
                self.set_result_message(result_message % ("", "Not Cache"))
                self.set_result(False)
        else:
            if headerchecker.check_feature(page.res_headers, headerchecker.TPU_CACHE, True):
                self.set_result_message(result_message % ("not", "Cache"))
                self.set_result(False)
            else:
                self.set_result_message(result_message % ("not", "Not Cache"))
                self.set_result(True)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class TimeStampChecker(SinglePageChecker):
    def __init__(self, expected_value, eq=False, case=None):
        super(CacheChecker, self).__init__(case)
        self._name = "TimeStampChecker"
        self._expected_value = expected_value
        self._eq = eq

    def is_ok(self, page):
        actually_timestamp = headerchecker.get_timestamp(page.res_headers)
        result_message = "checker name %s expected timestamp %s ;now timestamp %s" % (
            self._name, self._expected_value, actually_timestamp)
        self.set_result_message(result_message)
        if self.self._eq:
            if headerchecker.get_timestamp(page.res_headers) == self._expected_value:
                self.set_result(True)
            else:
                self.set_result(False)
        else:
            if headerchecker.get_timestamp(page.res_headers) == self._expected_value:
                self.set_result(False)
            else:
                self.set_result(True)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class ContentCountChecker(SinglePageChecker):
    def __init__(self, expected_content, expected_count, case):
        super(ContentCountChecker, self).__init__(case)
        self._name = "ContentCountChecker"
        self._expected_content = expected_content
        self._expected_count = expected_count

    def is_ok(self, page):
        actually_count = page.content.count(self._expected_content)
        self.set_result_message("checker name %s expected_content %s , expected_count is %s , actually %s" % (
            self._name, self._expected_content, self._expected_count, actually_count))
        if actually_count == self._expected_count:
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class ContentRegexChecker(SinglePageChecker):
    def __init__(self, expected_content, expected_count, case):
        super(ContentRegexChecker, self).__init__(case)
        self._name = "ContentRegexChecker"
        self._expected_content = expected_content
        self._expected_count = expected_count

    def is_ok(self, page):
        all_asset = re.findall(self._expected_content, page.content)
        actually_count = len(all_asset)
        self.set_result(actually_count == self._expected_count)
        if self.get_result():
            self.set_result_message(
                "checker name %s, test passed. expected pattern: %s, find: %s. expected count is %d , actual count is %d" % (
                    self._name, self._expected_content, ','.join(all_asset), self._expected_count, actually_count))
        else:
            self.set_result_message(
                "checker name %s, test failed. expected pattern: %s, expected count is %d , actual count is %d" % (
                    self._name, self._expected_content, self._expected_count, actually_count))
        return self.get_result()


class ContentRegexExistChecker(SinglePageChecker):
    def __init__(self, expected_content, case):
        super(ContentRegexExistChecker, self).__init__(case)
        self._name = "ContentRegexExistChecker"
        self._expected_content = expected_content

    def is_ok(self, page):
        m = re.search(self._expected_content, page.content)
        self.set_result(m)
        if self.get_result():
            self.set_result_message("checker name %s expected_content %s exists, %s, test passed." % (
                self._name, self._expected_content, m.group(0) ))
        else:
            self.set_result_message(
                "checker name %s expected_content %s not exists. test failed." % (self._name, self._expected_content ))
        return self.get_result()


class ResponseHeaderExistChecker(SinglePageChecker):
    def __init__(self, expected_headername, expect_exist=True, case=None):
        super(ResponseHeaderExistChecker, self).__init__(case)
        self._name = "ResponseHeaderExistChecker"
        self._expected_headername = expected_headername.lower()
        self._expect_exist = expect_exist

    def is_ok(self, page):
        reponse_headers = page.res_headers
        actually_exist = reponse_headers.get(self._expected_headername)
        if actually_exist:
            actually_exist = True
        else:
            actually_exist = False
        self.set_result_message("checker name %s ; headername %s ,expected exist :%s  actually: %s" % (
            self._name, self._expected_headername, self._expect_exist, actually_exist))
        if actually_exist == self._expect_exist:
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class ResponseHeaderChecker(SinglePageChecker):
    def __init__(self, expected_headername, expected_value, expected_eq=True, case=None):
        super(ResponseHeaderChecker, self).__init__(case)
        self._name = "ResponseHeaderExistChecker"
        self._expected_headername = expected_headername.lower()
        self._expected_value = expected_value.lower()
        self._expected_eq = expected_eq

    def is_ok(self, page):
        reponse_headers = page._res_headers

        actually_value = reponse_headers.get(self._expected_headername, None)
        self.set_result_message(
            "checker name %s ; headername %s ,expected value :%s  actually value: %s, expected_eq %s" % (
                self._name, self._expected_headername, self._expected_value, actually_value, self._expected_eq))

        if not actually_value:
            self.set_result_message(
                "checker name %s ; headername %s ,expected value :%s  actually value: there is no such head" % (
                    self._name, self._expected_headername, self._expected_value))
            self.set_result(False)
            return self.get_result()

        actually_eq = actually_value.lower() == self._expected_value.lower()
        self.set_result_message(
            "checker name %s ; headername %s ,expected value :%s  actually value: %s, expected_eq %s ,actually %s" % (
                self._name, self._expected_headername, self._expected_value, actually_value, self._expected_eq,
                actually_eq))
        if self._expected_eq and actually_eq:
            self.set_result(True)
        elif (not self._expected_eq) and (not actually_eq):
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class ResponseHeaderContainChecker(SinglePageChecker):
    def __init__(self, expected_headername, expected_value, expected_contain=True, case=None):
        super(ResponseHeaderContainChecker, self).__init__(case)
        self._name = "ResponseHeaderContainChecker"
        self._expected_headername = expected_headername.lower()
        self._expected_value = expected_value.lower()
        self._expected_contain = expected_contain

    def is_ok(self, page):
        reponse_headers = page._res_headers

        actually_value = reponse_headers.get(self._expected_headername, None)
        self.set_result_message(
            "checker name %s ; headername %s ,expected value :%s  actually value: %s, expected_contain %s" % (
                self._name, self._expected_headername, self._expected_value, actually_value, self._expected_contain))

        if not actually_value:
            self.set_result_message(
                "checker name %s ; headername %s ,expected value :%s  actually value: there is no such head" % (
                    self._name, self._expected_headername, self._expected_value))
            self.set_result(False)
            return self.get_result()

        actually_contain = (self._expected_value.lower() in actually_value.lower())
        self.set_result_message(
            "checker name %s ; headername %s ,expected value :%s  actually value: %s, expected_contain %s ,actually %s" % (
                self._name, self._expected_headername, self._expected_value, actually_value, self._expected_contain,
                actually_contain))
        if self._expected_contain and actually_contain:
            self.set_result(True)
        elif (not self._expected_contain) and (not actually_contain):
            self.set_result(True)
        else:
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()


class ImageBitSizeCheck(SinglePageChecker):
    def __init__(self, bit_size, exact_equal=False, case=None):
        super(ImageBitSizeCheck, self).__init__(case)
        self._bit_size = bit_size
        self._exact_equal = exact_equal
        self._case = case
        self._name = "ImageBitSizeCheck"

    def is_ok(self, page):
        bit_size_after_compress = string.atoi(page.res_headers.get('Content-Length'))
        result = None
        if self._exact_equal:
            result = ( self._bit_size == bit_size_after_compress )
        else:
            result = ( self._bit_size > bit_size_after_compress )

        message = "check name %s; image url: %s; expected bit size:%d bytes, actually bit size: %d bytes" % (
            self._name, page.url, self._bit_size, bit_size_after_compress)
        self.set_result(result);
        self.set_result_message(message)
        self._case.debug_message(self.get_result_message())
        return result


class ImageSizeCheck(SinglePageChecker):
    def __init__(self, width, height, case=None):
        super(ImageSizeCheck, self).__init__(case)
        self._width = width
        self._height = height
        self._case = case
        self._name = "ImageSizeCheck"

    def is_ok(self, page):
        (x, y) = self.get_image_size(page)
        result = (x == self._width and y == self._height)
        message = "check name %s; image url: %s; expected size:(%d,%d) actually size: (%d,%d)" % (
            self._name, page.url, self._width, self._height, x, y)
        self.set_result(result);
        self.set_result_message(message)
        self._case.debug_message(self.get_result_message())
        return result

    def get_image_size(self, page):
        # download images after optimized
        if os.path.exists("test.image"):
            os.remove("test.image")

        f = open('test.image', 'wb+')
        f.write(page.content)
        f.close()
        # Width and Height compare
        (x, y) = Image.open('test.image').size
        os.remove('test.image')

        return (x, y)


'''
@param transformer_type: 0 remove 1 replace 2 move 3 insert
@param selector_id: the #id of selected html tag to transform
@param before_id: the previous html tag's #id of the html tag after transform, optional.
@param after_id: the next html tag's #id of the html tag to transform, optional.
@param enabled: whether or not selector_id will be transformed. often used for chunked test case,
          eg. when html tag contained in more chunks, and merger field is false, this html tag would not be replaced
@param case: the case for checking

if the html tag to replace is the first html tag, then use after_id.
if the html tag to replace is the last html tag, then use before_id.
for the middle html tag, can use either of them or both
'''


class TransformerCheck(SinglePageChecker):
    def __init__(self, transformer_type, selector_id, before_id=None, after_id=None, enabled=True, case=None):
        super(TransformerCheck, self).__init__(case)
        self._enabled = enabled
        self._transformer_type = transformer_type
        self._selector_id = selector_id
        self._before_id = before_id
        self._after_id = after_id
        self._case = case
        self._name = "TransformerCheck"

    # return which html tag will do transformer, or None if not found
    def get_transformer_element(self, page):
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(page.content), parser)
        find_elements = etree.XPath('//*[@id=$ID]')
        if self._transformer_type == 0:
            elements = find_elements(tree, ID=self._selector_id)
            if len(elements) == 0:
                return None
            return elements[0]
        else:
            if self._selector_id:
                elements = find_elements(tree, ID=self._selector_id)
                if len(elements) == 0:
                    return None
                return elements[0]
            if self._before_id:
                elements = find_elements(tree, ID=self._before_id)
                if len(elements) == 0:
                    return None
                before_element = elements[0]

                while before_element.getnext().text.find("TRANSFORMER") > 0:
                    before_element = before_element.getnext()
                return before_element.getnext()

            if self._after_id:
                elements = find_elements(tree, ID=self._after_id)
                if len(elements) == 0:
                    return None
                after_element = elements[0]

                while after_element.getprevious().text.find("TRANSFORMER") > 0:
                    after_element = after_element.getprevious()
                return after_element.getprevious()


'''
@param selector_id: the #id of selected html tag to remove
@param enabled: whether or not selector_id will be removed. often used for chunked test case,
          when html tag contained in more chunks, and merger field is false, this html tag would not be removed
@param case: the case for checking
'''


class TransformerRemoveCheck(TransformerCheck):
    def __init__(self, selector_id, enabled=True, case=None):
        super(TransformerRemoveCheck, self).__init__(0, selector_id, None, None, enabled, case)
        self._name = "TransformerRemoveCheck"

    def is_ok(self, page):
        result = self.is_element_removed(page)
        self.set_result(result == self._enabled)
        self.set_result_message(
            "check name:%s; page url: %s; expected the element #%s is %s and actually the element is %s" %
            (self._name, page.url, self._selector_id, "removed" if self._enabled else "not removed",
             "removed" if result else "not removed" ))
        # self._case.debug_message(self.get_result_message())
        return self.get_result()

    def is_element_removed(self, page):
        return self.get_transformer_element(page) == None


'''
@param selector_id: the #id of selected html tag to replace
@param before_id: the previous html tag's #id of the html tag to replace, optional.
@param after_id: the next html tag's #id of the html tag to replace, optional.
@param content: the html tag's content after replace
@param enabled: whether or not selector_id will be removed. often used for chunked test case,
          when html tag contained in more chunks, and merger field is false, this html tag would not be replaced
@param case: the case for checking

if the html tag to replace is the first html tag, then use after_id.
if the html tag to replace is the last html tag, then use before_id.
for the middle html tag, can use either of them or both
'''


class TransformerReplaceCheck(TransformerCheck):
    def __init__(self, selector_id, before_id, after_id, content, enabled=True, case=None):
        super(TransformerReplaceCheck, self).__init__(1, selector_id, before_id, after_id, enabled, case)
        self._content = content
        self._name = "TransformerReplaceCheck"

    def is_ok(self, page):
        result = self.is_element_replaced(page)
        self.set_result(result == self._enabled)
        self.set_result_message(
            "check name: %s; page url: %s; expected the element #%s is %s with content '%s' and actually the element is %s" %
            (self._name, page.url, self._selector_id, "replaced" if self._enabled else "not replaced", self._content,
             "replaced" if result else "not replaced"))
        # self._case.debug_message(self.get_result_message())
        return self.get_result()

    def is_element_replaced(self, page):
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(page.content), parser)
        find_elements = etree.XPath('//*[@id=$ID]')

        # selector_id is removed
        elements = find_elements(tree, ID=self._selector_id)
        if len(elements) != 0:
            return False

        if self.get_transformer_element(page) == None:
            return False

        return self.get_transformer_element(page).text.strip().find(self._content.strip()) >= 0


'''
@param selector_id: the #id of selected html tag to move
@param before_id: previous html tag's id after move the selected html tag to new place, optional.
@param after_id: next html tag's id after move the selected html tag to new place, optional.
@param enabled: whether or not selector_id will be moved. often used for chunked test case,
          when html tag contained in more chunks, and merger field is false, this html tag would not be moved
@param case: the case for checking
'''


class TransformerMoveCheck(TransformerCheck):
    def __init__(self, selector_id, before_id=None, after_id=None, enabled=True, case=None):
        super(TransformerMoveCheck, self).__init__(2, selector_id, before_id, after_id, enabled, case)
        self._name = "TransformerMoveCheck"

    def is_ok(self, page):
        result = self.is_element_moved(page)
        self.set_result(result == self._enabled)
        self.set_result_message(
            "check name: %s; page url: %s; expected the element #%s is %s and actually the element is %s"
            % (self._name, page.url, self._selector_id, "moved" if self._enabled else "not moved",
               "replaced" if result else "not replaced"))
        # self._case.debug_message(self.get_result_message())
        return self.get_result()

    def is_element_moved(self, page):
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(page.content), parser)
        find_elements = etree.XPath('//*[@id=$ID]')

        elements = find_elements(tree, ID=self._selector_id)
        source_element = elements[0]

        return source_element is self.get_transformer_element(page)


'''
@param before_id: the previous html tag's #id of the inserted html tag, optional.
@param after_id: the next html tag's #id of the inserted html tag, optional.
@param content: the inserted html tag's content
@param enabled: whether or not selector_id will be removed. often used for chunked test case,
          when html tag contained in more chunks, and merger field is false, this html tag would not be replaced
@param case: the case for checking

if the html tag to replace is the first html tag, then use after_id.
if the html tag to replace is the last html tag, then use before_id.
for the middle html tag, can use either of them or both
'''


class TransformerInsertCheck(TransformerCheck):
    def __init__(self, before_id, after_id, content, enabled=True, case=None):
        super(TransformerInsertCheck, self).__init__(3, None, before_id, after_id, enabled, case)
        self._content = content
        self._name = "TransformerInsertCheck"

    def is_ok(self, page):
        result = self.is_element_inserted()
        self.set_result(result == self._enabled)
        self.set_result_message(
            "check name: %s; page url: %s; expected the element with content '%s' is %s and actually the element is %s"
            % (self._name, page.url, self._content, "inserted" if self._enabled else "not inserted",
               "inserted" if result else "not inserted"))
        # self._case.debug_message(self.get_result_message())
        return self.get_result()

    def is_element_inserted(self, page):
        if self.get_transformer_element(page) == None:
            return False

        return self.get_transformer_element(page).text.strip().find(self._content.strip()) >= 0


'''
@param before_id: the previous html tag's #id of the inserted html tag, optional.
@param after_id: the next html tag's #id of the inserted html tag, optional.
@param content: the inserted html tag's content
@param enabled: whether or not selector_id will be removed. often used for chunked test case,
          when html tag contained in more chunks, and merger field is false, this html tag would not be replaced
@param case: the case for checking

if the html tag to replace is the first html tag, then use after_id.
if the html tag to replace is the last html tag, then use before_id.
for the middle html tag, can use either of them or both
'''


class TransformerSurroundCheck(TransformerCheck):
    def __init__(self, selector_id=None, before_id=None, after_id=None, surround_tag=None, enabled=True, case=None):
        super(TransformerSurroundCheck, self).__init__(transformer_type=4, selector_id=selector_id, before_id=before_id,
                                                       after_id=after_id, enabled=enabled, case=case)
        self._selector_id = selector_id
        self._surround_tag = surround_tag
        self._name = "TransformerSurroundCheck"

    def is_ok(self, page):
        element = self.get_transformer_element(page)
        if element == None:
            self.set_result(False)
            self.set_result_message("these is not such element for %s" % self._selector_id)
        else:
            surround_tag = element.getparent().tag
            if surround_tag == self._surround_tag:
                self.set_result(True)
                self.set_result_message(
                    "elements with id %s is surround by %s " % ( self._selector_id, self._surround_tag))
            else:
                self.set_result(False)
                self.set_result_message(
                    "elements with id %s is not surround by %s " % ( self._selector_id, self._surround_tag))

        return self.get_result()

    def is_element_surrended(self, page):
        if self.get_transformer_element(page) == None:
            return False

        return self.get_transformer_element(page).text.strip().find(self._content.strip()) >= 0


class ResponsiveImageRewriteCheck2(SinglePageChecker):
    def __init__(self, os_src=None, delay_type="lazy", yo_src=[], case=None):
        self._os_src = os_src
        self._delay_type = delay_type
        self._yo_src = yo_src
        self._case = case
        self._name = "ResponsiveImageRewriteCheck2"

    def is_ok(self, page):
        for tag in self._yo_src:
            expected_content = "<img src=\"%s\" data-yo-delayType=\"%s\" data-yo-src=\"%s\" />" % (
                self._os_src, self._delay_type, tag)
            m = re.search(expected_content, page.content)
            if not m:
                self.set_result_message(
                    "checker name %s expected_content %s exists == %s " % (self._name, expected_content, m ))
                self.set_result(False)
            else:
                self.set_result_message(
                    "checker name %s expected_content %s exists == %s" % (self._name, expected_content, m ))
                self.set_result(True)


# refer http://www.cnblogs.com/descusr/archive/2012/06/20/2557075.html
class ResponsiveImageRewriteCheck(SinglePageChecker):
    after_shock_script_text = """(function(){function H(a,b){if(!1==t(a,this,function(c,e)"""

    def __init__(self, is_defer=False, insert_js=True, icon_url=None, exclude_images=[], case=None):
        super(ResponsiveImageRewriteCheck, self).__init__(case)
        self._is_defer = is_defer
        self._icon_url = icon_url
        self._insert_js = insert_js
        self._exclude_images = exclude_images
        self._name = "ResponsiveImageRewriteCheck"

    def is_ok(self, page):
        # as lxml will not parse <html> and <body> node, replace it
        content = page.content.replace("<html>", "<thtml>").replace("</html>", "</thtml>").replace("<body>",
                                                                                                   "<tbody>").replace(
            "</body>", "</tbody>")
        doc = etree.HTML(content.decode('utf-8'))

        if self._insert_js:
            after_shock_script = doc.xpath(u'//script[1]')
            if len(after_shock_script) == 0:
                self.set_result(False)
                self.set_result_message("check name: %s; AfterShocK script not insert in the front of the page body."
                                        % (self._name))
                return False

            after_shock_script = after_shock_script[0]
            if self.after_shock_script_text not in after_shock_script.text:
                self.set_result(False)
                self.set_result_message("check name: %s; AfterShocK script text not same as defined."
                                        % (self._name))
                return self.get_result()

            self.set_result(True)
            self.set_result_message(
                "check name: %s; AfterShocK script insert in the front of the page body and text is same as defined." % (
                    self._name))
        else:
            after_shock_script = doc.xpath(u'//script[1]')
            if len(after_shock_script) > 0:
                self.set_result(False)
                self.set_result_message(
                    "check name: %s; disabled jsInsert, AfterShocK script will not insert in the front of the page body but actually it is inserted."
                    % (self._name))
                return False
            else:
                self.set_result(True)
                self.set_result_message(
                    "check name: %s; disabled jsInsert, AfterShocK script will not insert in the front of the page body but actually it is not inserted."
                    % (self._name))

        all_images = doc.xpath(u"//img")
        # data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
        # check all images except exception list with attributes data-yo-delayType and data-yo-src
        for img in all_images:
            if img.attrib.has_key('data-yo-delaytype') and img.attrib.has_key('data-yo-src'):
                # check if in exclude list
                for exclude_img in self._exclude_images:
                    if img.attrib['data-yo-src'].find(exclude_img) >= 0:
                        self.set_result(False)
                        self.set_result_message(
                            "check name: %s; expected image %s not did responsiveImage as it is in exception list and actually it did"
                            % (self._name, img.attrib['data-yo-src']))
                        return self.get_result()

                # check icon url
                if self._icon_url:
                    if img.attrib.has_key('src') and img.attrib['src'] == self._icon_url:
                        self.set_result(True)
                        self.set_result_message(
                            "check name: %s; expected image %s iconUrl is %s and actually its iconUrl is it"
                            % (self._name, img.attrib['data-yo-src'], self._icon_url))
                    else:
                        self.set_result(False)
                        self.set_result_message(
                            "check name: %s; expected image %s iconUrl is %s and actually its iconUrl is not it"
                            % (self._name, img.attrib['data-yo-src'], self._icon_url))
                        return self.get_result()
                else:
                    pix_data_url = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
                    if img.attrib.has_key('src') and img.attrib['src'] == pix_data_url:
                        self.set_result(True)
                        self.set_result_message(
                            "check name: %s; image %s expected iconUrl is 1 pix image and actually its iconUrl is 1 pix image"
                            % (self._name, img.attrib['data-yo-src']))
                    else:
                        self.set_result(False)
                        self.set_result_message(
                            "check name: %s; image %s expected iconUrl is 1 pix image and actually its iconUrl is not 1 pix image"
                            % (self._name, img.attrib['data-yo-src']))
                        return self.get_result()

                if not self._is_defer:
                    self.set_result(img.attrib['data-yo-delaytype'] == 'lazy')
                    self.set_result_message(
                        "check name: %s; image %s expected image data-yo-delayType set is lazy and actually the set is %s"
                        % (self._name, img.attrib['data-yo-src'], "lazy" if self.get_result() else "not lazy"))
                else:
                    self.set_result(img.attrib['data-yo-delaytype'] == 'defer')
                    self.set_result_message(
                        "check name: %s; image %s expected image data-yo-delayType set is defer and actually the set is %s"
                        % (self._name, img.attrib['data-yo-src'], "defer" if self.get_result() else "not defer"))

                # check data-yo-src is not dataURIed
                self.set_result(img.attrib['data-yo-src'].find("data:image") < 0)
                self.set_result_message(
                    "check name: %s; image %s expected data-yo-src not dataURIed and actually it is %s"
                    % (self._name, img.attrib['data-yo-src'], "not dataURIed" if self.get_result() else "dataURIed"))

                if not self.get_result(): break
            else:
                if img.attrib.has_key('src') and img.attrib['src'].find('data:image') >= 0:
                    self.set_result(True)
                    self.set_result_message(
                        "check name: %s; image %s have dataURIed, expected not do responsiveImage and actually not do. "
                        % (self._name, img.attrib['src']))
                else:
                    # check if in exclude list
                    is_exclude = False
                    for exclude_img in self._exclude_images:
                        # check src or name attributes
                        if (img.attrib.has_key('src') and img.attrib['src'].find(exclude_img) >= 0) or \
                                (img.attrib.has_key('name') and img.attrib['name'].find(exclude_img) >= 0):
                            self.set_result(True)
                            self.set_result_message(
                                "check name: %s; image %s in exception list. expected it not do responsiveImage and actually not do responsiveImage"
                                % (self._name, img.attrib['src'] if img.attrib.has_key('src') else img.attrib['name']))
                            is_exclude = True
                            break

                    if not is_exclude:
                        self.set_result(False)
                        self.set_result_message(
                            "check name: %s; image %s expected all images set data-yo-delayType and data-yo-src and actually the image not set"
                            % (self._name, img.attrib['src']))
                        return self.get_result()

        if self.get_result():
            self.set_result_message("check name: %s; responsiveImage check passed." % self._name)

        return self.get_result()


# refer http://www.cnblogs.com/descusr/archive/2012/06/20/2557075.html
class ResponsiveImageDisplayNowCheck(SinglePageChecker):
    def __init__(self, displayNow_selector, displayNow_location="before", case=None):
        super(ResponsiveImageDisplayNowCheck, self).__init__(case)
        self._displayNow_selector = displayNow_selector
        self._displayNow_location = displayNow_location
        self._name = "ResponsiveImageDisplayNowCheck"


    def is_ok(self, page):
        # as lxml will not parse <html> and <body> node, replace it
        content = page.content.replace("<html>", "<thtml>").replace("</html>", "</thtml>").replace("<body>",
                                                                                                   "<tbody>").replace(
            "</body>", "</tbody>")
        doc = etree.HTML(content.decode('utf-8'))

        all_image = doc.xpath(u"//img")

        # check displayNow() place in correct position
        displayNow_script_tags = doc.xpath(u'/descendant::script[text()="window.yo_displayNow();"]')
        if not displayNow_script_tags or len(displayNow_script_tags) == 0:
            self.set_result(False)
            self.set_result_message("check name: %s. <script>window.yo_displayNow();<script> not found" % (self._name))
            return self.get_result()

        if len(displayNow_script_tags) > 1:
            self.set_result(False)
            self.set_result_message(
                "check name: %s. <script>window.yo_displayNow();<script> more than 1" % (self._name))
            return self.get_result()

        displayNow_script_tag = displayNow_script_tags[0]

        # find the tag which displayNow_selector specified, #id, .myclass, script[attribute=value]
        displayNow_tags = htmlparser.get_html_tags_by_selector(doc, self._displayNow_selector)
        if not displayNow_tags or len(displayNow_tags) == 0:
            self.set_result(False)
            self.set_result_message(
                "check name: %s. the element specified by %s not found" % (self._name, self._displayNow_selector))
            return self.get_result()

        displayNow_tag = displayNow_tags[0]
        if self._displayNow_location == "before":
            result = ( displayNow_tag.getprevious() == displayNow_script_tag )
            self.set_result(result)
            self.set_result_message("check name: %s; expected displayNow script before %s and actually %s" % (
                self._name, self._displayNow_selector, "yes" if self.get_result() else "no"))
        elif self._displayNow_location == "after":
            result = ( displayNow_tag.getnext() == displayNow_script_tag )
            self.set_result(result)
            self.set_result_message("check name: %s; expected displayNow script after %s and actually %s" % (
                self._name, self._displayNow_selector, "yes" if self.get_result() else "no"))
        elif self._displayNow_location == "prepend":
            result = ( displayNow_tag.getchildren()[0] == displayNow_script_tag )
            self.set_result(result)
            self.set_result_message("check name: %s; expected displayNow script prepend %s and actually %s" % (
                self._name, self._displayNow_selector, "yes" if self.get_result() else "no"))
        elif self._displayNow_location == "append":
            result = ( displayNow_tag.getchildren()[-1] == displayNow_script_tag )
            self.set_result(result)
            self.set_result_message("check name: %s; expected displayNow script append %s and actually %s" % (
                self._name, self._displayNow_selector, "yes" if self.get_result() else "no"))

        if self.get_result():
            self.set_result_message("check name: %s; responsiveImage check passed." % self._name)

        return self.get_result()


class ImageDataUriCheck(SinglePageChecker):
    # original_image_selector: #id, .myclass, tag[attr=value], tag[attr~value], tag[~value] to specify the image
    # image_dataURIed: image.src value after dataURIed
    def __init__(self, original_image_selector, image_dataURIed, case=None):
        super(ImageDataUriCheck, self).__init__(case)
        self._original_image_selector = original_image_selector
        self._image_dataURIed = image_dataURIed
        self._name = "ImageDataUriCheck"

    def is_ok(self, page):
        # after dataURIed, the original image will remove.
        doc = etree.HTML(page.content.decode('utf-8'))
        data_uri_images = htmlparser.get_html_tags_by_selector(doc, "img[src=%s]" % self._image_dataURIed)
        if len(data_uri_images) == 1:
            self.set_result(True)
            self.set_result_message(
                "check name: %s; expected the image %s will be dataURIed and actually it is dataURIed" % (
                    self._name, self._original_image_selector))

        if not self.get_result():
            self.set_result_message(
                "check name: %s; expected the image %s will be dataURIed and actually it is not dataURIed" % (
                    self._name, self._original_image_selector))
        else:
            self.set_result_message("check name: %s; test passed." % (self._name))

        return self.get_result()


# style attribute with img, will do dataUri. eg <div style="width:138px;height:42px;background-image:url(img/1.jpg)"></div>
class StyleDataUriCheck(SinglePageChecker):
    # original_selector: #id, .myclass, tag[attr=value], tag[attr~value], tag[~value] to specify the image
    # image_dataURIed: image.src value after dataURIed
    def __init__(self, style_selector, selector_tag_name, image_dataURIed, case=None):
        super(StyleDataUriCheck, self).__init__(case)
        self._style_selector = style_selector
        self._image_dataURIed = image_dataURIed
        self._selector_tag_name = selector_tag_name
        self._name = "StyleDataUriCheck"

    def is_ok(self, page):
        # after dataURIed, the original image will remove.
        doc = etree.HTML(page.content.decode('utf-8'))

        data_uri_styles = htmlparser.get_html_tags_by_selector(doc, "%s[style~%s]" % (
            self._selector_tag_name, self._image_dataURIed))
        if len(data_uri_styles) == 1:
            self.set_result(True)
            self.set_result_message("check name: %s; expected the %s will be dataURIed and actually it is dataURIed" % (
                self._name, self._style_selector))

        if not self.get_result():
            self.set_result_message(
                "check name: %s; expected the %s will be dataURIed and actually it is not dataURIed" % (
                    self._name, self._style_selector))
        else:
            self.set_result_message("check name: %s; test passed." % (self._name))

        return self.get_result()


# for inline css which has image url, will do dataUri. eg. 3.css will rewrite to 3.css.Y$DU.css, img/1.gif will do dataUri
# <style type="text/css">
# @import url("style/3.css");
# .inline1{
# width:138px;
# height:42px;
#     background-image: url(img/1.gif);
#     }
# </style>

# for external css, its content will do dataUri.
# eg. <link rel="stylesheet" type="text/css" href="style/1.css" />

class CssDataUriCheck(SinglePageChecker):
    def __init__(self, css_selector, inlined=True, sub_csses=[], sub_images=[], case=None):
        super(CssDataUriCheck, self).__init__(case)
        self._css_selector = css_selector
        self._sub_csses = sub_csses
        self._sub_images = sub_images
        self._inlined = inlined
        self._name = "CssDataUriCheck"

    def is_ok(self, page):
        doc = etree.HTML(page.content.decode('utf-8'))
        style_css = htmlparser.get_html_tags_by_selector(doc, self._css_selector)

        if len(style_css) == 0:
            self.set_result(False)
            self.set_result_message(
                "check name: %s; not found css by css_selector: %s" % (self._name, self._css_selector))
            return self.get_result()

        css_text = None
        if self._inlined:
            css_text = style_css[0].text
        else:
            css_url = style_css[0].attrib['href']
            if css_url.find(".Y$DU.css") >= 0:
                httpclient0 = httpclient(css_url, proxy_ip=ENV.get_all_values()["tpu_ip"], custom_headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"})
                page = httpclient0.get()
                css_text = page.content
            else:
                self.set_result(False)
                self.set_result_message("check name: %s; link href %s did not dataUri." % (self._name, css_url))
                return self.get_result()

        for sub_css in self._sub_csses:
            if sub_css.find(".Y$DU.css") < 0:
                sub_css = sub_css + ".Y$DU.css"
            if css_text.find(sub_css) < 0:
                self.set_result(False)
                self.set_result_message(
                    "check name: %s; not found sub css %s in css_selector body" % (self._name, sub_css))
                return self.get_result()
            else:
                self.set_result(True)
                self.set_result_message(
                    "check name: %s; found sub css %s in css_selector body. test passed" % (self._name, sub_css))

        for sub_image in self._sub_images:
            if css_text.find(sub_image) < 0:
                self.set_result(False)
                self.set_result_message(
                    "check name: %s; not found sub image %s in css_selector body." % (self._name, sub_image))
                return self.get_result()
            else:
                self.set_result(True)
                self.set_result_message(
                    "check name: %s; found sub image %s in css_selector body. test passed" % (self._name, sub_image))

        self.set_result(True)
        self.set_result_message("check name: %s; style css did dataUri for all sub css and sub images." % (self._name))

        return True


class CssUrlRewriteCheck(SinglePageChecker):
    def __init__(self, css_selector, inlined=False, rewrite_regex=None, expected_match_count=1, case=None):
        super(CssUrlRewriteCheck, self).__init__(case)
        self._css_selector = css_selector
        self._inlined = inlined
        self._rewrite_regex = rewrite_regex
        self._expected_match_count = expected_match_count
        self._name = "CssUrlRewriteCheck"

    def is_ok(self, page):
        doc = etree.HTML(page.content.decode('utf-8'))
        style_css = htmlparser.get_html_tags_by_selector(doc, self._css_selector)

        if len(style_css) == 0:
            self.set_result(False)
            self.set_result_message(
                "check name: %s; not found css by css_selector: %s" % (self._name, self._css_selector))
            return self.get_result()

        css_text = None
        if self._inlined:
            css_text = style_css[0].text
        else:
            css_url = style_css[0].attrib['href']
            css_url = htmlparser.make_full_url(css_url)
            httpclient0 = httpclient(css_url, proxy_ip=ENV.get_all_values()["tpu_ip"], custom_headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"})
            page = httpclient0.get()
            css_text = page.content

        matches = re.findall(self._rewrite_regex, css_text)
        actual_match_count = len(matches)
        self.set_result(actual_match_count == self._expected_match_count)
        if self.get_result():
            self.set_result_message(
                "check name: %s; test passed. expected # of rewrite css: %d, actual # of rewrite css: %d, the css rewrited to: %s." % (
                    self._name, self._expected_match_count, actual_match_count, ','.join(matches)))
        else:
            self.set_result_message(
                "check name: %s; test failed. expected # of rewrite css: %d, actual # of rewrite css: %d" % (
                    self._name, self._expected_match_count, actual_match_count))

        return self.get_result()


# check <!-- END OF YOTTAA PREFETCH LOCATION=<body> -->
class ClientPrefetchTagCheck(SinglePageChecker):
    def __init__(self, locationExpression, case=None):
        super(ClientPrefetchTagCheck, self).__init__(case)
        self._locationExpression = locationExpression
        self._name = "ClientPrefetchTagCheck"

    def is_ok(self, page):
        prefetch_tag = ("<!-- END OF YOTTAA PREFETCH LOCATION=<%s> -->" % (self._locationExpression) )
        if page.content.find(prefetch_tag) < 0:
            self.set_result(False)
            self.set_result_message("check name: %s. the prefetch %s not found" % (self._name, prefetch_tag))
            return self.get_result()
        else:
            self.set_result_message("check name: %s. found the prefetch %s" % (self._name, prefetch_tag))

        self.set_result(True)
        self.set_result_message("check name: %s; ClientPrefetchTagCheck passed." % self._name)

        return self.get_result()


class AsyncJsCheck(SinglePageChecker):
    def __init__(self, async_js=[], case=None):
        super(AsyncJsCheck, self).__init__(case)
        self._async_js = async_js
        self._name = "AsyncJsCheck"

    def is_ok(self, page):
        for js in self._async_js:
            expected_content = ".script\(\"%s.*\"\)" % js
            m = re.search(expected_content, page.content)
            if not m:
                self.set_result_message(
                    "checker name %s expected_content %s exists == %s " % (self._name, expected_content, m ))
                self.set_result(False)
            else:
                self.set_result_message(
                    "checker name %s expected_content %s exists == %s" % (self._name, expected_content, m ))
                self.set_result(True)

        return self.get_result()


class ClientPrefetchAutoPrefetchImageCheck(SinglePageChecker):
    def __init__(self, yo_loader_tag, preload_image_patterns=[], exclude_image_patterns=[], case=None):
        super(ClientPrefetchAutoPrefetchImageCheck, self).__init__(case)
        self._yo_loader_tag = yo_loader_tag
        self._preload_image_patterns = preload_image_patterns
        self._exclude_image_patterns = exclude_image_patterns
        self._name = "ClientPrefetchAutoPrefetchImageCheck"

    def is_ok(self, page):
        #print page.content
        doc = etree.HTML(page.content.decode('utf-8'))
        image_preload_script = htmlparser.get_html_tags_by_selector(doc, self._yo_loader_tag)
        if len(image_preload_script) > 0:
            self.set_result_message("check name: %s. found the prefetch %s" % (self._name, self._yo_loader_tag))
            image_preload_script = image_preload_script[0]
        else:
            self.set_result(False)
            self.set_result_message("check name: %s. the prefetch %s not found" % (self._name, self._yo_loader_tag))
            return self.get_result()

        yo_loader_text = image_preload_script.text
        for p in self._preload_image_patterns:
            if len(re.findall(p, yo_loader_text)) == 0:
                self.set_result(False)
                self.set_result_message("check name: %s. image %s not preloaded." % (self._name, p))
                return self.get_result()
            elif len(re.findall(p, yo_loader_text)) > 1:
                self.set_result(False)
                self.set_result_message(
                    "check name: %s. image %s preloaded duplicated, should only preload once." % (self._name, p))
                return self.get_result()
            else:
                self.set_result_message("check name: %s. image %s preloaded." % (self._name, p))

        for p in self._exclude_image_patterns:
            if len(re.findall(p, yo_loader_text)) == 0:
                self.set_result(True)
                self.set_result_message("check name: %s. image %s in exclude list not preloaded." % (self._name, p))
            else:
                self.set_result(False)
                self.set_result_message("check name: %s. image %s in exclude list preloaded. " % (self._name, p))
                return self.get_result()

        self.set_result(True)
        self.set_result_message("check name: %s. test passed." % (self._name))
        return self.get_result()


class ClientPrefetchSetCookieCheck(SinglePageChecker):
    def __init__(self, expected_content, httpOnly_sensitive=False, client=None, case=None):

        super(ClientPrefetchSetCookieCheck, self).__init__(case)
        self._httpOnly_sensitive = httpOnly_sensitive
        self._expected_content = expected_content
        self._client = client.copy()
        self._name = "ClientPrefetchSetCookieCheck"

    def get_cookie_url(self, str_cookie):
        i_start = str_cookie.find("\"")
        i_end = str_cookie.find("\"", i_start + 1)
        return str_cookie[i_start + 1: i_end]

    def is_ok(self, page):
        #print page.content
        doc = etree.HTML(page.content.decode('utf-8'))
        cookie_preload_script = None
        if self._httpOnly_sensitive:
            cookie_preload_script = htmlparser.get_html_tags_by_selector(doc, "script[~yo-app-sequencer]")
        else:
            cookie_preload_script = htmlparser.get_html_tags_by_selector(doc, "script[~cookie]")

        if len(cookie_preload_script) > 0:
            self.set_result_message("check name: %s. found the cookie preload script." % (self._name))
            cookie_preload_script = cookie_preload_script[0]

            text = cookie_preload_script.text
            if len(re.findall(self._expected_content, text)) > 0:
                self.set_result(True)
                self.set_result_message(
                    "check name: %s. found the expected_content %s" % (self._name, self._expected_content))
            else:
                self.set_result(False)
                self.set_result_message(
                    "check name: %s. not found the expected_content %s" % (self._name, self._expected_content))
        else:
            self.set_result(False)
            self.set_result_message(
                "check name: %s. not found the cookie preload script." % (self._name, self._yo_loader_tag))

        if self._httpOnly_sensitive:
            cookie_url = self.get_cookie_url(cookie_preload_script.text)
            from urlparse import urljoin

            full_url = urljoin(self._client.url, cookie_url)
            self._client.url = full_url
            page = self._case.query_url(self._client)
            checker = ResponseHeaderChecker(expected_headername="Set-Cookie", expected_value=self._expected_content,
                                            expected_eq=True, case=self._case)
            self.set_result(checker.is_ok(page))
            if self.get_result():
                self.set_result_message("cookie url %s success get cookie" % full_url)
            else:
                self.set_result_message("cookie url %s not get cookie" % full_url)

        return self.get_result()


class OpitmizatoinsBitMapCheck(SinglePageChecker):
    ( VARNISH_CACHE, TPU_CACHE, DISTRIBUTE_CACHE, COMPRESSION, MINIFICATION,
      PNGCRUSH, SPRITE, PREFETCH, URLREWRITE, DATAURI,
      ASYNCJS, CONCATENATION, IMAGERESIZE, IMAGETRANSCODING, IMAGECOMPRESSION,
      LAZYLOAD, EXCLUSION, HTMLINSERT, INSTANTON, INLINE
    ) = range(1, 21)

    def __init__(self, expected_ob=None, expected_value=True, case=None):
        super(OpitmizatoinsBitMapCheck, self).__init__(case)
        self._expected_ob = expected_ob
        self._expected_value = expected_value

    def is_ok(self, page):
        if self._expected_value:
            if headerchecker.check_feature(page.res_headers, self._expected_ob, True):
                self.set_result_message("ob index %s setting correct" % self._expected_ob)
                self.set_result(True)
            else:
                self.set_result_message("ob index %s setting wrong" % self._expected_ob)
                self.set_result(False)
        else:
            if headerchecker.check_feature(page.res_headers, self._expected_ob, False):
                self.set_result_message("ob index %s setting correct" % self._expected_ob)
                self.set_result(True)
            else:
                self.set_result_message("ob index %s setting wrong" % self._expected_ob)
                self.set_result(False)


class ContenGzipCheck(SinglePageChecker):
    def __init__(self, expected_gzip=True, case=None):
        super(ContenGzipCheck, self).__init__(case)
        self._name = "ContenGzipCheck"
        self._expected_gzip = expected_gzip

    def is_ok(self, page):
        actually_gziped = False
        if page.raw_data:
            if page.raw_data[:2] == "\x1f\x8b":
                actually_gziped = True
            else:
                actually_gziped = False
        else:
            self.set_result(False)
            self.set_result_message("there is no row data in page ,should use client support raw data")

        self.set_result_message(
            "content is expected gzip=%s , actually gzip=%s " % (self._expected_gzip, actually_gziped))
        if self._expected_gzip:
            if actually_gziped:
                self.set_result(True)
            else:
                self.set_result(False)
        else:
            if actually_gziped:
                self.set_result(False)
            else:
                self.set_result(True)

        return self.get_result()


class OptimizationBitCheck(SinglePageChecker):
    def __init__(self, index=headerchecker.TPU_CACHE, expected_value=True, case=None):
        '''
        index is form right to left should use headerchecker。constant
        expected_value := True or False
        '''
        super(OptimizationBitCheck, self).__init__(case)
        self._name = "OptimizationBitCheck"
        self._index = index
        self._expected_value = expected_value

    def is_ok(self, page):
        actually_value = headerchecker.check_feature(page.res_headers, self._index, True)

        result_message = "checker name %s expected index:%s valuse %s , actually " % (
            self._name, self._index, self._expected_value)

        if self._expected_value == actually_value:
            self.set_result(True)
            self.set_result_message(result_message + "same")
        else:
            self.set_result(False)
            self.set_result_message(result_message + "different")


class IndexPositionCheck(SinglePageChecker):
    def __init__(self, content_1, content_2, position_before=True, case=None):
        super(IndexPositionCheck, self).__init__(case)
        self._name = "IndexPositionCheck"
        self._content_1 = content_1
        self._content_2 = content_2
        self._position_before = position_before

    def is_ok(self, page):
        content = page.content
        index_1 = content.find(self._content_1)
        index_2 = content.find(self._content_2)

        actual_before = index_1 < index_2

        if self._position_before:
            if actual_before:
                self.set_result(True)
                self.set_result_message("content_1 %s expected before content_2 %s ,actually before")
            else:
                self.set_result(False)
                self.set_result_message("content_1 %s expected before content_2 %s ,actually after")
        else:
            if actual_before:
                self.set_result(False)
                self.set_result_message("content_1 %s expected after content_2 %s ,actually before")
            else:
                self.set_result(True)
                self.set_result_message("content_1 %s expected after content_2 %s ,actually after")


class ShardingCheck(SinglePageChecker):
    def __init__(self, expected_sharding=True, sharding_size=4, urls=[], case=None):
        '''
        '''
        super(ShardingCheck, self).__init__(case)
        self._name = "ShardingCheck"
        self._expected_sharding = expected_sharding
        self._sharding_size = sharding_size - 1
        self._urls = urls

    def get_sharding_size(self, url):
        return int(re.findall(".*cdn-.*-([0-%s])\..*" % self._sharding_size, url)[0])

    def match_sharding(self, url):
        return re.match(".*cdn-.*-([0-9])\..*", url)

    def is_ok(self, page):
        all_link = htmlparser.get_all_links(page)
        max_sharding_size = 0
        for link in all_link:
            if self._expected_sharding:
                cur_size = self.get_sharding_size(link)
                if cur_size > max_sharding_size:
                    max_sharding_size = cur_size
            else:
                if self.match_sharding(link):
                    self.set_result(False)
                    self.set_result_message("execpted no domainsharding ,but has domainsharding url %s " % link)
                    return
                else:
                    self.set_result(True)
                    self.set_result_message("execpted no domainsharding ,and not domainsharding url %s " % link)
        if self._expected_sharding:
            if self._sharding_size == max_sharding_size:
                self.set_result(True)
                self.set_result_message("execpted no domainsharding size %s and max doamin sharding size is %s " % (
                    self._sharding_size, max_sharding_size))
            else:
                self.set_result(False)
                self.set_result_message("execpted no domainsharding size %s and max doamin sharding size is %s " % (
                    self._sharding_size, max_sharding_size))


class XYottaaChecker(SinglePageChecker):
    def __init__(self, xyottaa_exist=True, cdn_exist=False, case=None):
        '''
        '''
        super(XYottaaChecker, self).__init__(case)
        self._name = "XYottaaChecker"
        self._xyottaa_exist = xyottaa_exist
        self._cdn_exist = cdn_exist


    def is_ok(self, page):
        expected_keys = ["X-Yottaa-Metrics", "X-Yottaa-Optimizations", "profile.id", "profile.name", "resource.version",
                         "adn.id", "shard.size"]
        if self._cdn_exist:
            expected_keys.append("cdn.hostname")

        for key in expected_keys:
            elements = htmlparser.get_element_by_attr(page, "name", key)
            if self._xyottaa_exist:
                if len(elements) == 1:
                    self.set_result(True)
                    self.set_result_message("the meta tag %s existed " % elements[0].get('content'))
                elif len(elements) > 1:
                    self.set_result(False)
                    self.set_result_message("has muti meta tag %s existed " % key)
                    break
                else:
                    self.set_result(False)
                    self.set_result_message("no meta tag %s existed " % key)
                    break
            else:
                if len(elements) == 0:
                    self.set_result(True)
                    self.set_result_message("the meta tag %s not existed " % key)
                else:
                    self.set_result(False)
                    self.set_result_message("the meta tag %s  existed " % key)
                    break


class SetCookieChecker(SinglePageChecker):
    def __init__(self, cookie_name=None, cookie_value=None, expected_same=True, case=None):
        super(SetCookieExistChecker, self).__init__(case)
        self._name = "SetCookieChecker"
        self._cookie_name = cookie_name
        self._cookie_value = cookie_value
        self._expected_same = expected_same

    def is_ok(self, page):
        cookies = page.cookies
        actually_value = cookies.get(name=self._cookie_name)

        actually_same = True

        if actually_value == self._cookie_value:
            actually_same = True
        else:
            actually_same = False

        message = "the expected cookie is %s:%s ; actually cookes %s .expected existed %s; actually %s"
        message = message % (self._cookie_name, self._cookie_value, cookies, self._expected_exist, actually_same )

        if actually_same == self._expected_same:
            self.set_result(True)
        else:
            self.set_result(False)

        self.set_result_message(message)
        return self.get_result()


class SetCookieExistChecker(SinglePageChecker):
    def __init__(self, cookie_name=None, expected_exist=True, case=None):
        super(SetCookieExistChecker, self).__init__(case)
        self._name = "SetCookieChecker"
        self._cookie_name = cookie_name
        self._expected_exist = expected_exist

    def is_ok(self, page):
        message = "the expected cookie is %s ; actually cookes %s .expected existed %s; actually %s"

        cookies = page.cookies
        if not cookies:
            if self._expected_exist:
                self.set_result(False)
                message = message % (self._cookie_name, cookies, self._expected_exist, False )
                self.set_result_message(message)
                return self.get_result()
            else:
                self.set_result(True)
                message = message % (self._cookie_name, cookies, self._expected_exist, False )
                self.set_result_message(message)
                return self.get_result()

        actually_exist = True
        if self._cookie_name in cookies.keys():
            actually_exist = True
        else:
            actually_exist = False

        message = message % (self._cookie_name, cookies, self._expected_exist, actually_exist )
        if actually_exist == self._expected_exist:
            self.set_result(True)
        else:
            self.set_result(False)

        self.set_result_message(message)
        return self.get_result()


class GoThroughNodeChecker(SinglePageChecker):
    def __init__(self, node_id=None, expected_go_through=True, case=None):
        super(GoThroughNodeChecker, self).__init__(case)
        self._name = "GoThroughNodeChecker"
        self._node_id = node_id
        self._expected_go_through = expected_go_through

    def is_ok(self, page):
        all_node_id = headerchecker.get_metrics(page._res_headers)

        actually_go_through = True
        message = "the expected nodeid is %s ; all gothrough nodeid is %s .expected go through %s; actually %s"
        if self._node_id in all_node_id:
            actually_go_through = True
        else:
            actually_go_through = False

        message = message % (self._node_id, all_node_id, self._expected_go_through, actually_go_through)

        if self._expected_go_through == actually_go_through:
            self.set_result(True)
        else:
            self.set_result(False)

        self.set_result_message(message)
        return self.get_result()


class StaticSessionNodeChecker(SinglePageChecker):
    def __init__(self, node_id=None, expected_same=True, case=None):
        super(StaticSessionNodeChecker, self).__init__(case)
        self._name = "StaticSessionNodeChecker"
        self._node_id = node_id
        self._expected_same = expected_same

    def is_ok(self, page):
        static_session_node = headerchecker.get_static_sessioin_node(page.cookies)

        actually_same = True
        message = "the nodeid is %s ; nodeid from cookie is %s .expected same %s; actually %s"
        if static_session_node == self._node_id:
            actually_same = True
        else:
            actually_same = False

        message = message % (self._node_id, static_session_node, self._expected_same, actually_same)

        if self._expected_same == actually_same:
            self.set_result(True)
        else:
            self.set_result(False)

        self.set_result_message(message)
        return self.get_result()


class StaticSessionOriginChecker(SinglePageChecker):
    def __init__(self, origin_id=None, expected_same=True, case=None):
        super(StaticSessionOriginChecker, self).__init__(case)
        self._name = "StaticSessionOriginChecker"
        self._origin_id = origin_id
        self._expected_same = expected_same

    def is_ok(self, page):
        static_session_node = headerchecker.get_static_sessioin_node(page.cookies)

        actually_same = True
        message = "the originid is %s ; originid from cookie is %s .expected same %s; actually %s"
        if static_session_node == self._origin_id:
            actually_same = True
        else:
            actually_same = False

        message = message % (self._origin_id, static_session_node, self._expected_same, actually_same)

        if self._expected_same == actually_same:
            self.set_result(True)
        else:
            self.set_result(False)

        self.set_result_message(message)
        return self.get_result()


class AssetVersionCheck(SinglePageChecker):
    sys_profile_version = 0
    custom_profile_version = 1
    group_version = 2
    asset_version = 3


    def __init__(self, version_type=None, expected_version=0, url=None, case=None, new_assetversion=True):
        '''
        '''
        super(AssetVersionCheck, self).__init__(case)
        self._name = "AssetVersionCheck"
        self._version_type = version_type
        self._expected_version = expected_version
        self._url = url
        self._reg = "(v~[^/]*)"
        self._newassetversion = new_assetversion

    def get_all_versions(self):
        all_versions = re.findall(self._reg, self._url)
        assert len(all_versions) == 1
        version = all_versions[0][2:]
        return version

    def get_version_by_type(self, version_type):
        version = self.get_all_versions()
        return version.split(".")[version_type]


    def is_ok(self, page):
        actuall_version = self.get_version_by_type(self._version_type)
        result_message = "the url is %s , check versions %s , expected_version %s, actually version %s ,they are same %s" % (
            self._url, self._version_type, self._expected_version, actuall_version, "%s")
        if str(actuall_version) == str(self._expected_version):
            result_message_real = result_message % (True)
            self.set_result(True)
        else:
            result_message_real = result_message % (False)
            self.set_result(False)
        self.set_result_message(result_message_real)
        return self.get_result()

    def VersionBitCheck(self, expected_versionbit):
        if 'v~' not in self._url:
            result_message = "Check version in url %s, there is no version in url  %s" % (self._url, "%s")
            self.set_result_message(result_message)
            if '0' == str(expected_versionbit):
                result_message_real = result_message % (True)
                self.set_result(True)
            else:
                result_message_real = result_message % (False)
                self.set_result(False)
            self.set_result_message(result_message_real)
            return self.get_result()
        else:
            actuall_version = self.get_all_versions(self)
            result_message = "Check version in url %s, actual version is: %s, expected version bit is: %s  %s" % (
                self._url, actuall_version, expected_versionbit, "%s")
            if len(actuall_version.split(".")) == expected_versionbit:
                result_message_real = result_message % (True)
                self.set_result(True)
            else:
                result_message_real = result_message % (False)
                self.set_result(False)
            self.set_result_message(result_message_real)
            return self.get_result()


    def is_ok(self, page):
        if self._newassetversion:
            actuall_version = self.get_version_by_type(self._version_type)
            result_message = "the url is %s , check versions index [%s] , expected_version %s, actually version %s ,they are same %s" % (
                self._url, self._version_type, self._expected_version, actuall_version, "%s")
            if str(actuall_version) == str(self._expected_version):
                result_message_real = result_message % (True)
                self.set_result(True)
            else:
                result_message_real = result_message % (False)
                self.set_result(False)
            self.set_result_message(result_message_real)
        else:
            actuall_version = self.get_all_versions(self)
            result_message = "the url is %s, check new asset version not enable. actual version is: %s. " % (
                self._url, actuall_version)
            if len(actuall_version.split(".")) == 2:
                result_message_real = result_message % (True)
                self.set_result(True)
            else:
                result_message_real = result_message % (False)
                self.set_result(False)
            self.set_result_message(result_message_real)
        return self.get_result()


class LargeAssetRedirectCheck(SinglePageChecker):
    def __init__(self, param_name=None, location_param_value=None, url=None, case=None):
        super(LargeAssetRedirectCheck, self).__init__(case)
        self._name = "LargeAssetRedirectCheck"
        self._param_name = param_name
        self._location_param_value = location_param_value
        self._url = url
        self._reg = "(v~[^/]*)"

    def get_actuallocation(self, page):
        return page.res_headers._store["location"][1]

    def is_ok(self, page):
        actual_location = self.get_actuallocation(page)
        result_message = "checker name: LargeAssetRedirectCheck ; the location is %s , check %s, expected : %s in location, actual :  %s" % (
            actual_location, self._param_name, self._location_param_value, "%s")
        if self._location_param_value in actual_location:
            result_message_real = result_message % (True)
            self.set_result(True)
        else:
            result_message_real = result_message % (False)
            self.set_result(False)
        self.set_result_message(result_message_real)
        return self.get_result()


class LogicAndChecker(SinglePageChecker):
    def __init__(self, checklist=None, case=None):
        '''
        '''
        super(LogicAndChecker, self).__init__(case)
        self._checklist = checklist

    def is_ok(self, page):
        for checker in self._checklist:
            checker.is_ok(page)
            if not checker.get_result():
                self.set_result(False)
                self.set_result_message("the checker %s is fall : sub checker message %s" % (
                    checker.get_name(), checker.get_result_message()))
                return False

        self.set_result(True)
        self.set_result_message("all sub checker are pass")
        return True

class AfterShockCheck(SinglePageChecker):
    after_shock_script_text = """(function(){function H(a,b){if(!1==t(a,this,function(c,e)"""

    def __init__(self, insert_js=True, aftershockjs=None, case=None):
        super(AfterShockCheck, self).__init__(case)
        self._insert_js = insert_js
        self._aftershockjs = aftershockjs
        self._name = "AfterShockCheck"

    def is_ok(self, page):
        # as lxml will not parse <html> and <body> node, replace it
        content = page.content.replace("<html>", "<thtml>").replace("</html>", "</thtml>").replace("<body>",
                                                                                                   "<tbody>").replace(
            "</body>", "</tbody>")
        doc = etree.HTML(content.decode('utf-8'))

        if self._insert_js:
            after_shock_script = doc.xpath(u'//script[1]')
            if len(after_shock_script) == 0:
                self.set_result(False)
                self.set_result_message("check name: %s; AfterShocK script not insert in the front of the page body."
                                        % (self._name))
                return False

            after_shock_script = after_shock_script[0]
            if self._aftershockjs is not None:
                if self._aftershockjs in after_shock_script.text:
                    self.set_result(True)
                    self.set_result_message("check name: %s; AfterShocK script text same as defined. Expected contained insertjs is: %s, Actual is: %s"
                                        % (self._name, self._aftershockjs, after_shock_script.text))
                    return self.get_result()
            if self.after_shock_script_text not in after_shock_script.text:
                self.set_result(False)
                self.set_result_message("check name: %s; AfterShocK script text not same as defined. Expected contained insertjs is: %s, Actual is: %s"
                                        % (self._name, self.after_shock_script_text, after_shock_script.text))
                return self.get_result()

            self.set_result(True)
            self.set_result_message(
                "check name: %s; AfterShocK script insert in the front of the page body and text is same as defined. Actual inserted js is: %s"
                % (self._name, after_shock_script.text))
        else:
            after_shock_script = doc.xpath(u'//script[1]')

            if len(after_shock_script) == 0:
                self.set_result(True)
                self.set_result_message("check name: %s; AfterShocK script not insert in the front of the page body."
                                        % (self._name))
                return True

            after_shock_script = after_shock_script[0]
            if self.after_shock_script_text in after_shock_script.text:
                self.set_result(False)
                self.set_result_message(
                    "check name: %s; disabled jsInsert, AfterShocK script will not insert in the front of the page, actually it is inserted."
                    % (self._name))
                return self.get_result()

            else:
                self.set_result(True)
                self.set_result_message(
                    "check name: %s; disabled jsInsert, AfterShocK script will not insert in the front of the page, actually it is not inserted."
                    % (self._name))
                return self.get_result()

            self.set_result(True)
            self.set_result_message("check name: %s; AfterShocK script wasn't inserted in the front of the page body and text." % (self._name))

class PageContentCheck(SinglePageChecker):
    def __init__(self, case=None, pageContent=None):
        super(PageContentCheck, self).__init__(case)
        self._pageContent = pageContent
        self._name = "PageContentCheck"

    def is_ok(self, page=None):
        if page:
            self._page = page
        if self._page.content and self._page.content != "":
            if self._pageContent in self._page.content:
                self.set_result_message("checker name %s Expected contained content: %s, Page content is: %s" % (self._name, self._pageContent, self._page.content))
                self.set_result(True)
            else:
                self.set_result_message("checker name %s There is not the content in the page. Expected contain: %s. Page content is: %s" % (self._name, self._pageContent, self._page.content))
                self.set_result(False)
        else:
            self.set_result_message("checker name %s There is no page content. Page content is: %s" % (self._name, self._page.content))
            self.set_result(False)

        self._case.debug_message(self.get_result_message())
        return self.get_result()

class BasetagCheck(SinglePageChecker):
    def __init__(self, url=None, contain_string=None, case=None):
        '''
        '''
        super(BasetagCheck, self).__init__(case)
        self._name = "BasetagCheck"
        self._contain_string = contain_string
        self._url = url
        self._reg = "(v~[^/]*)"

    def is_ok(self, page=None):
        result_message = "checker name: BasetagCheck; the url is %s , check domain, expected contain string: %s, contains %s" % (
            self._url, self._contain_string, "%s")
        if self._contain_string in self._url:
            result_message_real = result_message % (True)
            self.set_result(True)
        else:
            result_message_real = result_message % (False)
            self.set_result(False)

        self.set_result_message(result_message_real)
        return self.get_result()
