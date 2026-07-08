import unittest

from textnode import TextNode, TextType , text_node_to_html_node , split_nodes_delimiter , extract_markdown_images, extract_markdown_links , split_nodes_image , split_nodes_link , text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
        
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("Part 2 baby `code block 2` worddd", TextType.TEXT)
        node3 = TextNode("this text will be bold", TextType.BOLD)  
        
        new_nodes_1 = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes_2 = split_nodes_delimiter([node2] , "`" , TextType.CODE)
        new_nodes_3 = split_nodes_delimiter([node3] , "**" , TextType.BOLD)
        
        self.assertEqual(new_nodes_1 , 
                        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
                         )
        self.assertEqual(new_nodes_3 , 
                         [
                             TextNode("this text will be bold", TextType.BOLD) 
                         ]
                         )
        
    def test_extract_markdown_images(self):
         # single image
        text = "This is an image ![cat](cat.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("cat", "cat.png")])

        # multiple images
        text = "![one](1.png) and ![two](2.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("one", "1.png"), ("two", "2.png")])

        # empty alt and url
        text = "![]()"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "")])

        # image inside text
        text = "start ![logo](/img/logo.svg) end"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("logo", "/img/logo.svg")])

        # should not match links
        text = "[Google](https://google.com)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

        # invalid (nested brackets blocked by regex)
        text = "![nested [alt]](img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
    
    def test_extract_markdown_links(self):
        # single link
        text = "Visit [Google](https://google.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Google", "https://google.com")])

        # multiple links
        text = "Visit [Google](https://www.google.com) and check [GitHub](https://github.com) for code"
        result = extract_markdown_links(text)

        self.assertEqual(
            result,
            [
                ("Google", "https://www.google.com"),
                ("GitHub", "https://github.com"),
            ],
        )

        # empty text and url
        text = "[]()"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "")])

        # mixed image + link (should ignore image)
        text = "![img](img.png) [link](url)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "url")])

        # should not match images
        text = "![cat](cat.png)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

        # invalid (nested brackets blocked)
        text = "[nested [text]](url)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
        
    def test_split_nodes_image(self):
        image_cases = [
            (
                [TextNode("Hello ![cat](cat.png) world", TextType.TEXT)],
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("cat", TextType.IMAGE, "cat.png"),
                    TextNode(" world", TextType.TEXT),
                ],
            ),
            (
                [TextNode("![cat](cat.png) hello", TextType.TEXT)],
                [
                    TextNode("cat", TextType.IMAGE, "cat.png"),
                    TextNode(" hello", TextType.TEXT),
                ],
            ),
            (
                [TextNode("hello ![cat](cat.png)", TextType.TEXT)],
                [
                    TextNode("hello ", TextType.TEXT),
                    TextNode("cat", TextType.IMAGE, "cat.png"),
                ],
            ),
            (
                [TextNode("![cat](cat.png)", TextType.TEXT)],
                [
                    TextNode("cat", TextType.IMAGE, "cat.png"),
                ],
            ),
            (
                [TextNode("![one](1.png)![two](2.png)", TextType.TEXT)],
                [
                    TextNode("one", TextType.IMAGE, "1.png"),
                    TextNode("two", TextType.IMAGE, "2.png"),
                ],
            ),
            (
                [TextNode("A ![one](1.png) B ![two](2.png) C", TextType.TEXT)],
                [
                    TextNode("A ", TextType.TEXT),
                    TextNode("one", TextType.IMAGE, "1.png"),
                    TextNode(" B ", TextType.TEXT),
                    TextNode("two", TextType.IMAGE, "2.png"),
                    TextNode(" C", TextType.TEXT),
                ],
            ),
            (
                [TextNode("No image here", TextType.TEXT)],
                [
                    TextNode("No image here", TextType.TEXT),
                ],
            ),
            (
                [TextNode("this is [a link](https://boot.dev)", TextType.TEXT)],
                [
                    TextNode("this is [a link](https://boot.dev)", TextType.TEXT),
                ],
            ),
            (
                [TextNode("already image", TextType.IMAGE, "cat.png")],
                [
                    TextNode("already image", TextType.IMAGE, "cat.png"),
                ],
            ),
            (
                [
                    TextNode("A ![one](1.png)", TextType.TEXT),
                    TextNode("already link", TextType.LINK, "https://boot.dev"),
                    TextNode("B ![two](2.png) C", TextType.TEXT),
                ],
                [
                    TextNode("A ", TextType.TEXT),
                    TextNode("one", TextType.IMAGE, "1.png"),
                    TextNode("already link", TextType.LINK, "https://boot.dev"),
                    TextNode("B ", TextType.TEXT),
                    TextNode("two", TextType.IMAGE, "2.png"),
                    TextNode(" C", TextType.TEXT),
                ],
            ),
        ]

        for old_nodes, expected in image_cases:
            self.assertEqual(split_nodes_image(old_nodes), expected)
        
        
    def test_split_nodes_link(self):
        link_cases = [
            (
                [TextNode("Hello [boot dev](https://boot.dev) world", TextType.TEXT)],
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("boot dev", TextType.LINK, "https://boot.dev"),
                    TextNode(" world", TextType.TEXT),
                ],
            ),
            (
                [TextNode("[boot dev](https://boot.dev) hello", TextType.TEXT)],
                [
                    TextNode("boot dev", TextType.LINK, "https://boot.dev"),
                    TextNode(" hello", TextType.TEXT),
                ],
            ),
            (
                [TextNode("hello [boot dev](https://boot.dev)", TextType.TEXT)],
                [
                    TextNode("hello ", TextType.TEXT),
                    TextNode("boot dev", TextType.LINK, "https://boot.dev"),
                ],
            ),
            (
                [TextNode("[boot dev](https://boot.dev)", TextType.TEXT)],
                [
                    TextNode("boot dev", TextType.LINK, "https://boot.dev"),
                ],
            ),
            (
                [TextNode("[one](1.com)[two](2.com)", TextType.TEXT)],
                [
                    TextNode("one", TextType.LINK, "1.com"),
                    TextNode("two", TextType.LINK, "2.com"),
                ],
            ),
            (
                [TextNode("A [one](1.com) B [two](2.com) C", TextType.TEXT)],
                [
                    TextNode("A ", TextType.TEXT),
                    TextNode("one", TextType.LINK, "1.com"),
                    TextNode(" B ", TextType.TEXT),
                    TextNode("two", TextType.LINK, "2.com"),
                    TextNode(" C", TextType.TEXT),
                ],
            ),
            (
                [TextNode("No link here", TextType.TEXT)],
                [
                    TextNode("No link here", TextType.TEXT),
                ],
            ),
            (
                [TextNode("this is ![an image](image.png)", TextType.TEXT)],
                [
                    TextNode("this is ![an image](image.png)", TextType.TEXT),
                ],
            ),
            (
                [TextNode("already link", TextType.LINK, "https://boot.dev")],
                [
                    TextNode("already link", TextType.LINK, "https://boot.dev"),
                ],
            ),
            (
                [
                    TextNode("A [one](1.com)", TextType.TEXT),
                    TextNode("already image", TextType.IMAGE, "cat.png"),
                    TextNode("B [two](2.com) C", TextType.TEXT),
                ],
                [
                    TextNode("A ", TextType.TEXT),
                    TextNode("one", TextType.LINK, "1.com"),
                    TextNode("already image", TextType.IMAGE, "cat.png"),
                    TextNode("B ", TextType.TEXT),
                    TextNode("two", TextType.LINK, "2.com"),
                    TextNode(" C", TextType.TEXT),
                ],
            ),
        ]

        for old_nodes, expected in link_cases:
            self.assertEqual(split_nodes_link(old_nodes), expected)
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text) , expected)
        
    
        
if __name__ == "__main__":
    unittest.main()