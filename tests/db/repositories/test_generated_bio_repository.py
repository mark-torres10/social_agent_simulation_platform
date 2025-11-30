"""Tests for db.repositories.generated_bio_repository module."""

from unittest.mock import Mock

import pytest

from db.adapters.base import GeneratedBioDatabaseAdapter
from db.models import GeneratedBio
from db.repositories.generated_bio_repository import SQLiteGeneratedBioRepository


class TestSQLiteGeneratedBioRepositoryCreateOrUpdateGeneratedBio:
    """Tests for SQLiteGeneratedBioRepository.create_or_update_generated_bio method."""

    def test_creates_generated_bio_with_correct_values(self):
        """Test that create_or_update_generated_bio creates a bio with correct values."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        bio = GeneratedBio(
            handle="test.bsky.social",
            generated_bio="This is a test bio for the profile.",
            created_at="2024-01-01T00:00:00Z",
        )

        # Act
        result = repo.create_or_update_generated_bio(bio)

        # Assert
        assert result == bio
        mock_adapter.write_generated_bio.assert_called_once_with(bio)

    def test_creates_generated_bio_with_different_values(self):
        """Test that create_or_update_generated_bio handles different bio values correctly."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        bio = GeneratedBio(
            handle="another.bsky.social",
            generated_bio="This is a longer bio with more detailed information about the user and their interests.",
            created_at="2024-02-01T12:30:00Z",
        )

        # Act
        result = repo.create_or_update_generated_bio(bio)

        # Assert
        assert result.handle == "another.bsky.social"
        assert len(result.generated_bio) > 50
        mock_adapter.write_generated_bio.assert_called_once_with(bio)

    def test_persists_generated_bio_to_database(self):
        """Test that create_or_update_generated_bio persists the bio to the database via write_generated_bio."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        bio = GeneratedBio(
            handle="test.bsky.social",
            generated_bio="Test bio text",
            created_at="2024-01-01T00:00:00Z",
        )

        # Act
        result = repo.create_or_update_generated_bio(bio)

        # Assert
        mock_adapter.write_generated_bio.assert_called_once()
        call_args = mock_adapter.write_generated_bio.call_args[0][0]
        assert isinstance(call_args, GeneratedBio)
        assert call_args.handle == result.handle
        assert call_args.generated_bio == result.generated_bio
        assert call_args.created_at == result.created_at

    def test_creates_generated_bio_with_empty_handle(self):
        """Test that creating GeneratedBio with empty handle is allowed (no Pydantic validator)."""
        # Note: GeneratedBio model doesn't have handle validation, so empty string is technically allowed
        # The repository doesn't validate handle either since validation would happen at model creation
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        bio = GeneratedBio(
            handle="",
            generated_bio="Bio text",
            created_at="2024-01-01T00:00:00Z",
        )

        # Act
        result = repo.create_or_update_generated_bio(bio)

        # Assert
        # Model creation succeeds without validation error
        assert result.handle == ""
        mock_adapter.write_generated_bio.assert_called_once_with(bio)

    def test_creates_generated_bio_with_empty_generated_bio(self):
        """Test that creating GeneratedBio with empty generated_bio is allowed (no Pydantic validator)."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        bio = GeneratedBio(
            handle="test.bsky.social",
            generated_bio="",
            created_at="2024-01-01T00:00:00Z",
        )

        # Act
        result = repo.create_or_update_generated_bio(bio)

        # Assert
        # Model creation succeeds without validation error
        assert result.generated_bio == ""
        mock_adapter.write_generated_bio.assert_called_once_with(bio)

    @pytest.mark.parametrize(
        "error_message,check_identity",
        [
            ("Database error", False),
            ("DB error", True),
        ],
    )
    def test_propagates_adapter_exception(self, error_message, check_identity):
        """Test that create_or_update_generated_bio propagates adapter exceptions when database write fails."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        db_error = Exception(error_message)
        mock_adapter.write_generated_bio.side_effect = db_error
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        bio = GeneratedBio(
            handle="test.bsky.social",
            generated_bio="Test bio",
            created_at="2024-01-01T00:00:00Z",
        )

        # Act & Assert
        with pytest.raises(Exception, match=error_message) as exc_info:
            repo.create_or_update_generated_bio(bio)

        if check_identity:
            assert exc_info.value is db_error
        else:
            assert exc_info.value is mock_adapter.write_generated_bio.side_effect

    def test_propagates_original_exception_directly(self):
        """Test that create_or_update_generated_bio propagates the original exception directly."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        original_error = ValueError("Invalid data")
        mock_adapter.write_generated_bio.side_effect = original_error
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        bio = GeneratedBio(
            handle="test.bsky.social",
            generated_bio="Test bio",
            created_at="2024-01-01T00:00:00Z",
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid data") as exc_info:
            repo.create_or_update_generated_bio(bio)

        assert exc_info.value is original_error


class TestSQLiteGeneratedBioRepositoryGetGeneratedBio:
    """Tests for SQLiteGeneratedBioRepository.get_generated_bio method."""

    def test_returns_generated_bio_when_found(self):
        """Test that get_generated_bio returns a bio when it exists in the database."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        handle = "test.bsky.social"
        expected = GeneratedBio(
            handle=handle,
            generated_bio="This is a test bio.",
            created_at="2024-01-01T00:00:00Z",
        )
        mock_adapter.read_generated_bio.return_value = expected

        # Act
        result = repo.get_generated_bio(handle)

        # Assert
        assert result is not None
        assert result.handle == expected.handle
        assert result.generated_bio == expected.generated_bio
        assert result.created_at == expected.created_at
        mock_adapter.read_generated_bio.assert_called_once_with(handle)

    def test_returns_none_when_generated_bio_not_found(self):
        """Test that get_generated_bio returns None when bio does not exist."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        handle = "nonexistent.bsky.social"
        mock_adapter.read_generated_bio.return_value = None

        # Act
        result = repo.get_generated_bio(handle)

        # Assert
        assert result is None
        mock_adapter.read_generated_bio.assert_called_once_with(handle)

    def test_calls_read_generated_bio_with_correct_handle(self):
        """Test that get_generated_bio calls read_generated_bio with the correct handle parameter."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        handle = "test.bsky.social"
        mock_adapter.read_generated_bio.return_value = None

        # Act
        repo.get_generated_bio(handle)

        # Assert
        mock_adapter.read_generated_bio.assert_called_once_with(handle)

    def test_returns_generated_bio_with_all_fields(self):
        """Test that get_generated_bio returns a bio with all fields correctly populated."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        handle = "test.bsky.social"
        expected = GeneratedBio(
            handle=handle,
            generated_bio="This is a longer bio with multiple sentences and detailed information about the user's interests and background.",
            created_at="2024-03-15T14:30:00Z",
        )
        mock_adapter.read_generated_bio.return_value = expected

        # Act
        result = repo.get_generated_bio(handle)

        # Assert
        assert result is not None
        assert result.handle == handle
        assert len(result.generated_bio) > 50
        assert result.created_at == "2024-03-15T14:30:00Z"

    def test_raises_value_error_when_handle_is_empty(self):
        """Test that get_generated_bio raises ValueError when handle is empty."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)

        # Act & Assert
        with pytest.raises(ValueError, match="handle cannot be empty"):
            repo.get_generated_bio("")

        mock_adapter.read_generated_bio.assert_not_called()

    def test_raises_value_error_when_handle_is_whitespace(self):
        """Test that get_generated_bio raises ValueError when handle is whitespace."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)

        # Act & Assert
        with pytest.raises(ValueError, match="handle cannot be empty"):
            repo.get_generated_bio("   ")

        mock_adapter.read_generated_bio.assert_not_called()


class TestSQLiteGeneratedBioRepositoryListAllGeneratedBios:
    """Tests for SQLiteGeneratedBioRepository.list_all_generated_bios method."""

    def test_returns_empty_list_when_no_bios_exist(self):
        """Test that list_all_generated_bios returns an empty list when no bios exist."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        expected = []
        mock_adapter.read_all_generated_bios.return_value = expected

        # Act
        result = repo.list_all_generated_bios()

        # Assert
        assert result == expected
        assert isinstance(result, list)
        assert len(result) == 0
        mock_adapter.read_all_generated_bios.assert_called_once()

    def test_returns_all_generated_bios_when_bios_exist(self):
        """Test that list_all_generated_bios returns all bios from the database."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        expected = [
            GeneratedBio(
                handle="user1.bsky.social",
                generated_bio="Bio 1",
                created_at="2024-01-01T00:00:00Z",
            ),
            GeneratedBio(
                handle="user2.bsky.social",
                generated_bio="Bio 2",
                created_at="2024-01-02T00:00:00Z",
            ),
        ]
        mock_adapter.read_all_generated_bios.return_value = expected

        # Act
        result = repo.list_all_generated_bios()

        # Assert
        assert len(result) == 2
        assert result[0].handle == "user1.bsky.social"
        assert result[1].handle == "user2.bsky.social"
        assert result[0].generated_bio == "Bio 1"
        assert result[1].generated_bio == "Bio 2"

    def test_returns_bios_in_correct_order(self):
        """Test that list_all_generated_bios returns bios in the order provided by read_all_generated_bios."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        expected = [
            GeneratedBio(
                handle="first.bsky.social",
                generated_bio="First bio",
                created_at="2024-01-01T00:00:00Z",
            ),
            GeneratedBio(
                handle="second.bsky.social",
                generated_bio="Second bio",
                created_at="2024-01-02T00:00:00Z",
            ),
        ]
        mock_adapter.read_all_generated_bios.return_value = expected

        # Act
        result = repo.list_all_generated_bios()

        # Assert
        assert result[0].handle == "first.bsky.social"
        assert result[1].handle == "second.bsky.social"

    def test_calls_read_all_generated_bios_once(self):
        """Test that list_all_generated_bios calls read_all_generated_bios exactly once."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        mock_adapter.read_all_generated_bios.return_value = []

        # Act
        repo.list_all_generated_bios()

        # Assert
        mock_adapter.read_all_generated_bios.assert_called_once()

    def test_handles_large_number_of_bios(self):
        """Test that list_all_generated_bios handles a large number of bios correctly."""
        # Arrange
        mock_adapter = Mock(spec=GeneratedBioDatabaseAdapter)
        repo = SQLiteGeneratedBioRepository(mock_adapter)
        expected = [
            GeneratedBio(
                handle=f"user{i}.bsky.social",
                generated_bio=f"Bio {i}",
                created_at=f"2024-01-{i + 1:02d}T00:00:00Z",
            )
            for i in range(100)
        ]
        mock_adapter.read_all_generated_bios.return_value = expected

        # Act
        result = repo.list_all_generated_bios()

        # Assert
        assert len(result) == 100
        assert all(isinstance(bio, GeneratedBio) for bio in result)
        assert result[0].handle == "user0.bsky.social"
        assert result[99].handle == "user99.bsky.social"
