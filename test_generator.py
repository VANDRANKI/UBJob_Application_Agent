import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent


class TestGeneratorLoadsItsOwnEnv:
    """Regression: generator.py imports `load_dotenv` from python-dotenv but
    never calls it, then instantiates `client = OpenAI()` at import time,
    which reads OPENAI_API_KEY straight from the process environment. This
    only ever "worked" because main.py happens to import .config first, and
    config.py's own load_dotenv() call has the side effect of populating
    os.environ for every module imported afterwards in the same process --
    generator.py was silently relying on some other module to have already
    done its job. Importing generator.py on its own, before anything else
    has called load_dotenv(), crashed immediately with:

        openai.OpenAIError: The api_key client option must be set either by
        passing api_key to the client or by setting the OPENAI_API_KEY
        environment variable

    even though a perfectly valid OPENAI_API_KEY is sitting in .env right
    next to it. Reproduced by importing generator.py in a subprocess with a
    clean environment (no inherited OPENAI_API_KEY) so it can't accidentally
    piggyback on a load_dotenv() call some other already-imported module
    made in this same test process.
    """

    def test_importing_generator_alone_does_not_crash(self):
        env = os.environ.copy()
        env.pop("OPENAI_API_KEY", None)
        env.pop("OPENAI_MODEL", None)

        result = subprocess.run(
            [sys.executable, "-c", "import generator"],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            "importing generator.py on its own crashed:\n" + result.stderr
        )
