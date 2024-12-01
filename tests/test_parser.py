from pyplz.command import Parser


class TestParser:
    def test_parser_list(self):
        parser = Parser()

        cmd = parser.parse_args(["-l"])

        assert cmd.list
        assert not cmd.has_task_specified()
        assert not cmd.is_default()

    def test_parser_list_full(self):
        parser = Parser()

        cmd = parser.parse_args(["--list"])

        assert cmd.list
        assert not cmd.has_task_specified()
        assert not cmd.is_default()

    def test_parser_help(self):
        parser = Parser()

        cmd = parser.parse_args(["-h"])

        assert cmd.help
        assert not cmd.has_task_specified()
        assert not cmd.is_default()

    def test_parser_help_full(self):
        parser = Parser()

        cmd = parser.parse_args(["--help"])

        assert cmd.help
        assert not cmd.has_task_specified()
        assert not cmd.is_default()

    def test_parser_empty(self):
        parser = Parser()

        cmd = parser.parse_args([])

        assert not cmd.has_task_specified()
        assert cmd.is_default()

    def test_parser_task(self):
        parser = Parser()

        cmd = parser.parse_args(["some-task"])

        assert cmd.has_task_specified()
        assert cmd.args == []
        assert not cmd.is_default()

    def test_parser_task_with_args(self):
        parser = Parser()

        cmd = parser.parse_args(["some-task", "arg1", "arg2"])

        assert cmd.has_task_specified()
        assert cmd.args == ["arg1", "arg2"]
        assert not cmd.is_default()

    def test_parser_task_with_args_and_env(self):
        parser = Parser()

        cmd = parser.parse_args(["-e" "a=1", "some-task", "arg1", "arg2"])

        assert cmd.has_task_specified()
        assert cmd.args == ["arg1", "arg2"]
        assert cmd.env == [["a", "1"]]
        assert not cmd.is_default()

    def test_parser_task_with_args_and_env_mixed(self):
        parser = Parser()

        cmd = parser.parse_args(["some-task", "arg1", "-e", "a=1", "arg2"])

        assert cmd.has_task_specified()
        assert cmd.args == ["arg1", "arg2"]
        assert cmd.env == [["a", "1"]]
        assert not cmd.is_default()
