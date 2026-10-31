import libkcov
from libkcov import cobertura


class bash_sh_shebang(libkcov.TestCase):
    def runTest(self):
        rv, o = self.do(
            self.kcov
            + " --bash-handle-sh-invocation "
            + self.outbase
            + "/kcov "
            + self.sources
            + "/tests/bash/shell-main"
        )

        dom = cobertura.parseFile(self.outbase + "/kcov/shell-main/cobertura.xml")
        assert cobertura.hitsPerLine(dom, "sh-shebang.sh", 4) == 1


class bash_sh_shebang_arguments(libkcov.TestCase):
    def runTest(self):
        rv, o = self.do(
            self.kcov
            + " --bash-handle-sh-invocation "
            + self.outbase
            + "/kcov "
            + self.sources
            + "/tests/bash/shell-main"
        )

        dom = cobertura.parseFile(self.outbase + "/kcov/shell-main/cobertura.xml")
        assert cobertura.hitsPerLine(dom, "sh-shebang-args.sh", 4) == 1


class bash_sh_shebang_no_untraced_ps4(libkcov.TestCase):
    def runTest(self):
        rv, o = self.do(
            self.kcov
            + " --bash-handle-sh-invocation "
            + self.outbase
            + "/kcov "
            + self.sources
            + "/tests/bash/shell-main"
        )

        assert b"is not an integer" not in o


class bash_exit_before_child(libkcov.TestCase):
    def runTest(self):
        # kcovKcov shouldn't wait for the background process, so call it with kcovKcov = False
        rv, o = self.do(
            self.kcov
            + " --bash-tracefd-cloexec "
            + self.outbase
            + "/kcov "
            + self.sources
            + "/tests/bash/background-child.sh",
            kcovKcov=False,
            timeout=3.0,
        )
        self.assertEqual(0, rv, "kcov exited unsuccessfully")
        dom = cobertura.parseFile(self.outbase + "/kcov/background-child.sh/cobertura.xml")
        self.assertIsNone(cobertura.hitsPerLine(dom, "background-child.sh", 1))
        self.assertEqual(1, cobertura.hitsPerLine(dom, "background-child.sh", 3))
        self.assertEqual(1, cobertura.hitsPerLine(dom, "background-child.sh", 4))


class bash_ldpreload_multilib(libkcov.TestCase):
    def runTest(self):
        rv, o = self.do(
            self.kcov
            + " --bash-handle-sh-invocation --bash-tracefd-cloexec "
            + self.outbase
            + "/kcov "
            + self.sources
            + "/tests/bash/sh-shebang.sh"
        )
        self.assertEqual(0, rv, "kcov exited unsuccessfully")
        dom = cobertura.parseFile(self.outbase + "/kcov/sh-shebang.sh/cobertura.xml")
        self.assertIsNone(cobertura.hitsPerLine(dom, "sh-shebang.sh", 1))
        self.assertEqual(1, cobertura.hitsPerLine(dom, "sh-shebang.sh", 4))


class bash_nested_strings(libkcov.TestCase):
    # Old bash, as on macOS, may not parse quotes inside "$(...)" like this
    def runTest(self):
        rv, o = self.do(
            self.kcov + " " + self.outbase + "/kcov " + self.sources + "/tests/bash/nested-strings.sh"
        )

        dom = cobertura.parseFile(self.outbase + "/kcov/nested-strings.sh/cobertura.xml")

        for line in (5, 7, 9, 11, 18, 25, 27, 32, 38, 42, 44, 47, 52, 53, 57, 62, 69, 77, 81):
            assert cobertura.hitsPerLine(dom, "nested-strings.sh", line) == 1, line

        # String bodies, here document bodies and first lines of multi-line strings
        for line in (14, 15, 16, 21, 22, 23, 30, 35, 36, 39, 40, 48, 49, 50, 51, 54, 55, 56, 60, 65, 66, 72, 73, 74, 75, 78, 79):
            assert cobertura.hitsPerLine(dom, "nested-strings.sh", line) is None, line
