import unittest

from markdown_to_html import markdown_to_html_node
from markdown_to_html import paragraph_to_html_node
from markdown_to_html import heading_to_html_node
from markdown_to_html import code_to_html_node
from markdown_to_html import quote_to_html_node
from markdown_to_html import ul_to_html_node
from markdown_to_html import ol_to_html_node


class TestMarkdownToHtml(unittest.TestCase):

    def test_basic_paragraph_to_html_node(self):
        test_md_block = "this is a paragraph"
        result = paragraph_to_html_node(test_md_block)

        self.assertEqual(
            "<p>this is a paragraph</p>",
            result.to_html()
        )

    def test_basic_heading_to_html_node(self):
        test_md_headings = [
            "# this is an h1",
            "## this is an h2",
            "### this is an h3",
            "#### this is an h4",
            "##### this is an h5",
            "###### this is an h6"
        ]

        for i in range(0,len(test_md_headings)):
            result = heading_to_html_node(test_md_headings[i])
            h_val = i+1
            self.assertEqual(
                f"<h{h_val}>this is an h{h_val}</h{h_val}>",
                result.to_html()
            )

    def test_basic_code_to_html_node(self):
        test_code_block = "`this is some test code`"
        result = code_to_html_node(test_code_block)
        self.assertEqual(
            "<pre><code>this is some test code</code></pre>",
            result.to_html()
        )

    # def test_basic_quote_to_html_node(self):
    #     test_quote_block = "> this is a " \
    #                        "> multiline quote of something" \
    #                        "> very interesting"
        
    #     result = quote_to_html_node(test_quote_block)
    #     self.assertEqual(
    #         "<blockquote> this is a multiline quote of something very interesting</blockquote>",
    #         result.to_html()
    #     )

    # def test_basic_ul_to_html_node(self):
    #     test_ul_block = "- item 1\n" \
    #                     "- item 2\n" \
    #                     "- item 3\n"
        
    #     result = ul_to_html_node(test_ul_block)

    # def test_basic_ol_to_html_node(self):
    #     test_ol_block = "1. item 1\n" \
    #                     "2. item 2\n" \
    #                     "3. item 3\n"
    #     result = ol_to_html_node(test_ol_block)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    # def test_codeblock(self):
    #     md = """
    # ```
    # This is text that _should_ remain
    # the **same** even with inline stuff
    # ```
    # """

    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    #     )