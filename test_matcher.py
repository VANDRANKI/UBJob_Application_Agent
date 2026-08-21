from matcher import determine_resume_type, count_matches, KEYWORDS
from config import RESUME_PATHS


class TestCountMatches:
    """Regression: a raw `kw in text` substring check made the single-
    letter DATA skill keyword "R" match any text containing the letter
    "r" anywhere -- "or", "for", "are", "your" -- which is virtually every
    job description regardless of topic, and drowned out the "no matches"
    fallback in determine_resume_type."""

    def test_single_letter_keyword_does_not_match_inside_other_words(self):
        assert count_matches("completely unrelated text", ["R"]) == 0
        assert count_matches("looking for a grant writer", ["R"]) == 0

    def test_single_letter_keyword_matches_as_a_whole_word(self):
        assert count_matches("I use R and Python daily", ["R"]) == 1

    def test_multi_word_phrase_still_matches(self):
        assert count_matches("skilled in data analysis and ETL", ["data analysis", "ETL"]) == 2

    def test_case_insensitive(self):
        assert count_matches("PYTHON and sql", ["Python", "SQL"]) == 2


class TestDetermineResumeType:
    """Regression: KEYWORDS used "Associate" (mixed case) while every other
    category ("DATA", "RESEARCH") and every downstream consumer
    (config.RESUME_PATHS, generator._skills_highlight_by_resume_type) used
    all-caps "ASSOCIATE". The scores dict was hardcoded with "ASSOCIATE",
    so scores[category] += ... raised KeyError as soon as the loop reached
    the "Associate" entry from KEYWORDS -- on every single call, regardless
    of input, since that loop runs unconditionally over all categories."""

    def test_does_not_crash_on_any_input(self):
        # This used to raise KeyError('Associate') unconditionally.
        determine_resume_type("Data Analyst", "Python SQL data analysis")

    def test_data_role_title_wins(self):
        result = determine_resume_type("Data Scientist", "some unrelated description")
        assert result == "DATA"

    def test_research_skills_win(self):
        result = determine_resume_type(
            "Generic Title", "materials science nanotechnology XRD SEM"
        )
        assert result == "RESEARCH"

    def test_associate_role_title_is_matched_and_does_not_crash(self):
        """The exact case that used to guarantee a KeyError: a job title
        that matches the Associate category's role_types."""
        result = determine_resume_type("Program Associate", "coordination and administration")
        assert result == "ASSOCIATE"

    def test_no_matches_defaults_to_associate(self):
        result = determine_resume_type("Zzz Nonexistent Title", "completely unrelated text")
        assert result == "ASSOCIATE"

    def test_every_possible_return_value_has_a_resume_path(self):
        """The whole point of matching: main.py looks up
        RESUME_PATHS.get(resume_type) with whatever this function returns.
        Every category name this function can produce must be a real key
        in RESUME_PATHS, or resume selection silently returns None."""
        possible_returns = set(KEYWORDS.keys()) | {"ASSOCIATE"}
        for category in possible_returns:
            assert category in RESUME_PATHS, f"{category!r} has no matching resume path"

    def test_scores_keys_match_keywords_keys(self):
        """No hardcoded scores dict to drift out of sync with KEYWORDS again."""
        determine_resume_type("Research Scientist", "laboratory synthesis characterization")
