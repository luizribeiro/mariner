from unittest import TestCase
from unittest.mock import patch

from mariner.server.utils import retry


class RetryTest(TestCase):
    num_attempts: int = 0

    def setUp(self) -> None:
        self.sleep_patcher = patch("mariner.server.utils.time.sleep")
        self.sleep_patcher.start()

    def tearDown(self) -> None:
        self.sleep_patcher.stop()

    def test_fail_all_retries(self) -> None:
        def _always_fail() -> None:
            self.num_attempts += 1
            raise Exception()

        self.num_attempts = 0
        with self.assertRaises(Exception):
            retry(
                _always_fail,
                Exception,
                num_retries=2,
            )
        self.assertEquals(self.num_attempts, 3)

    def test_catch_a_different_exception(self) -> None:
        class A(Exception):
            ...

        class B(Exception):
            ...

        def _always_fail_with_b() -> None:
            self.num_attempts += 1
            raise B()

        self.num_attempts = 0
        with self.assertRaises(B):
            retry(
                _always_fail_with_b,
                A,
                num_retries=2,
            )
        self.assertEquals(self.num_attempts, 1)

    def test_success_fully_returns_after_two_attempts(self) -> None:
        def _fails_sometimes() -> None:
            self.num_attempts += 1
            if self.num_attempts == 1:
                raise Exception()
            return 42

        self.num_attempts = 0
        ret = retry(
            _fails_sometimes,
            Exception,
            num_retries=1,
        )
        self.assertEquals(self.num_attempts, 2)
        self.assertEquals(ret, 42)
