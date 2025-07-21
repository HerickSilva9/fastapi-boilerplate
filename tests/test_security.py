from argon2.exceptions import VerifyMismatchError
import pytest

from app.core.security import generate_hash, ph


def test_generate_hash():
    my_string = 'some-string'
    my_hash = generate_hash(my_string)

    assert isinstance(my_hash, str)
    assert my_hash != my_string
    assert ph.verify(my_hash, my_string)
    
    with pytest.raises(VerifyMismatchError) as exc_info:
        ph.verify(my_hash, 'diferent-string')
    
    error_msg = 'The password does not match the supplied hash'
    assert error_msg in str(exc_info.value)