import subprocess
import logging

from dmc_migrator.package_usage_detector import DMCUsageDetector


logger = logging.getLogger(__name__)


class DmcMigrator:

    def __init__(self, repo_path, old_version="0.12.1", target_version=None):
        self.repo_path = repo_path
        self.usage_detector = None
        self.usage_results = {}

        self._initialize_versions(old_version, target_version)

    def _initialize_versions(self, old_version, target_version):
        if not old_version:
            logger.error(
                "Please provide the old version of dash_mantine_components."
            )
        else:
            self.old_version = old_version

        if not target_version:
            # Get the current version of dash_mantine_components from the repo
            try:
                result = subprocess.run(
                    ["pip", "show", "dash_mantine_components"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                for line in result.stdout.splitlines():
                    if line.startswith("Version:"):
                        self.target_version = line.split(":")[1].strip()
                        break
            except subprocess.CalledProcessError:
                logger.error(
                    "Error: Could not determine the current version of dash_mantine_components."
                )
                self.target_version = None
        else:
            self.target_version = target_version

    def detect_dmc_usage(self):

        self.usage_detector = DMCUsageDetector(self.repo_path)
        self.usage_detector.run()
        self.usage_results = self.usage_detector.results

        return self.usage_results

    def get_usage_summary(self):
        """
        Generate a summary of dash_mantine_components usage.
        """
        if not self.usage_results:
            self.detect_dmc_usage()

        return self.usage_results

    def run(self):
        """
        Run the migration process
        """
        self.detect_dmc_usage()

        return self.get_usage_summary()


if __name__ == "__main__":
    migrator = DmcMigrator(repo_path="test_cases/current").run()
