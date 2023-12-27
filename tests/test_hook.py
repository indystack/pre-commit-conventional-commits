import re
import pytest
import os.path
import pre_commit_conventional_commits.hook as hook

TEST_PATH = os.path.abspath(os.path.dirname(__file__))

CUSTOM_TYPES = ["bug", "quirk"]


def get_path(path):
    return os.path.join(TEST_PATH, "commit_messages", path)


@pytest.fixture(autouse=True)
def cmd():
    return "pre-commit-conventional-commits"


@pytest.fixture(autouse=True)
def bad_message_path():
    return get_path("bad_commit_message")


@pytest.fixture(autouse=True)
def conventional_message_path():
    return get_path("conventional_commit_message")


@pytest.fixture(autouse=True)
def custom_message_path():
    return get_path("custom_commit_message")


class TestHooks:
    def test_given_custom_commit_types_when_calling_regex_types_it_will_include_custom_types(self):
        result = hook.regex_types(CUSTOM_TYPES)
        regex = re.compile(result)

        assert regex.match("bug")
        assert regex.match("quirk")

    def test_given_empty_scope_when_calling_regex_it_will_return_true(self):
        result = hook.regex_scope()
        regex = re.compile(result)

        assert regex.match("")

    def test_given_scope_inside_parantheses_when_calling_regex_scope_it_will_return_true(self):
        result = hook.regex_scope()
        regex = re.compile(result)

        # Without parantheses scope is not going to be matched
        result = regex.match("myscope")
        assert result.span() == (0, 0)

        # With parantheses scope is going to be matched
        result = regex.match("(myscope)")
        assert result.span() == (0, 9)

    def test_given_scope_with_special_characters_when_calling_regex_scope_it_will_return_true(self):
        result = hook.regex_scope()
        regex = re.compile(result)

        assert regex.match("(ci-tests)")
        assert regex.match("(ci:tests)")
        assert regex.match("(ci/tests)")
        assert regex.match("(ci tests)")
        assert regex.match("(ci_tests)")

    def test_given_delimiter_in_commit_message_when_calling_regex_delimiter_it_will_pass(self):
        result = hook.regex_delimiter()
        regex = re.compile(result)

        assert regex.match(":")

    def test_given_breaking_change_in_commit_message_when_calling_regex_delimiter_it_will_pass(self):
        result = hook.regex_delimiter()
        regex = re.compile(result)

        assert regex.match("!:")

    def test_given_subject_that_does_not_start_with_space_when_calling_regex_subject_it_will_fail(self):
        result = hook.regex_subject()
        regex = re.compile(result)

        assert not regex.match("subject")

    def test_given_subject_that_does_start_with_space_when_calling_regex_subject_it_will_pass(self):
        result = hook.regex_subject()
        regex = re.compile(result)

        assert regex.match(" subject")

    def test_given_conventional_commit_types_when_calling_hook_it_will_return_only_conventional_types(self):
        assert hook.convnetional_types_list() == hook.CONVENTIONAL_TYPES

    def test_given_additional_commit_types_when_calling_hook_it_will_include_custom_types(self):
        result = hook.convnetional_types_list(["superduper"])

        assert set(["superduper", *hook.CONVENTIONAL_TYPES]) == set(result)

    @pytest.mark.parametrize("type", hook.DEFAULT_TYPES)
    def test_given_each_type_from_default_types_when_calling_hook_it_will_return_true(self, type):
        input = f"{type}: commit message"

        assert hook.is_commit_conventional(input)

    @pytest.mark.parametrize("type", hook.CONVENTIONAL_TYPES)
    def test_given_each_type_from_conventional_types_when_calling_hook_it_will_return_true(self, type):
        input = f"{type}: commit message"

        assert hook.is_commit_conventional(input)

    @pytest.mark.parametrize("type", CUSTOM_TYPES)
    def test_given_each_type_from_custom_types_when_calling_hook_it_will_return_true(self, type):
        input = f"{type}: commit message"

        assert hook.is_commit_conventional(input, CUSTOM_TYPES)

    def test_given_breaking_change_in_commit_message_when_calling_hook_it_will_return_true(self):
        input = "fix!: commit message"

        assert hook.is_commit_conventional(input)

    def test_given_scope_in_commit_message_when_calling_hook_it_will_return_true(self):
        input = "fix(tests): commit message"

        assert hook.is_commit_conventional(input)

    def test_given_no_args_when_calling_main_execution_will_fail(self):
        result = hook.main()

        assert result == hook.RESULT_FAIL

    def test_given_invalid_commit_message_when_calling_main_it_will_return_result_fail(self, bad_message_path):
        result = hook.main([bad_message_path])

        assert result == hook.RESULT_FAIL

    def test_given_custom_commit_message_when_calling_main_it_will_return_result_fail(self, custom_message_path):
        result = hook.main([custom_message_path])

        assert result == hook.RESULT_FAIL

    def test_given_conventional_commit_message_when_calling_main_it_will_return_result_success(
        self, conventional_message_path
    ):
        result = hook.main([conventional_message_path])

        assert result == hook.RESULT_SUCCESS

    def test_given_custom_commit_message_and_custom_commit_types_when_calling_main_it_will_return_result_success(
        self, custom_message_path
    ):
        result = hook.main(["custom", custom_message_path])

        assert result == hook.RESULT_SUCCESS

    def test_given_conventional_commit_message_and_custom_commit_types_when_calling_main_it_will_return_result_success(
        self, conventional_message_path
    ):
        result = hook.main(["custom", conventional_message_path])

        assert result == hook.RESULT_SUCCESS

    def test_given_no_arguments_when_calling_subprocess_it_will_return_result_fail(self, capsys):
        hook.main()

        captured = capsys.readouterr()
        assert "the following arguments are required" in captured.err
