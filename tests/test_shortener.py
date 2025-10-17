from textwrap import dedent

from shorty.shortener import shorten_code


def test_removes_block_and_line_comments_cpp():
    source = dedent(
        """
        // Sample function
        int main() {
            /* multi
               line */
            return 42; // answer
        }
        """
    ).strip()
    expected = "int main() {\n    return 42;\n}\n"
    assert shorten_code(source, language="cpp") == expected


def test_preserves_python_strings_with_hash():
    source = dedent(
        """
        def greeting():
            return "Hello #world"  # comment
        """
    ).strip()
    expected = "def greeting():\n    return \"Hello #world\"\n"
    assert shorten_code(source, language="python") == expected


def test_ignores_url_like_comments():
    source = dedent(
        """
        // Visit http://example.com for details
        const char* url = "https://example.com"; // comment
        """
    ).strip()
    expected = "const char* url = \"https://example.com\";\n"
    assert shorten_code(source, language="cpp") == expected


def test_collapses_consecutive_blank_lines():
    source = dedent(
        """
        <div>


        <!-- comment -->
        <span>Text</span>

        </div>
        """
    ).strip()
    expected = "<div>\n<span>Text</span>\n</div>\n"
    assert shorten_code(source, language="html") == expected
