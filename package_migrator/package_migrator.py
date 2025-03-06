import subprocess
import logging

from package_migrator.package_usage_detector import PackageUsageDetector


logger = logging.getLogger(__name__)


class PackageMigrator:

    def __init__(self, repo_path, package_name, old_version=None, target_version=None):
        self.repo_path = repo_path
        self.package_name = package_name
        self.usage_detector = None
        self.usage_results = {}

        self._initialize_versions(old_version, target_version)

    def _initialize_versions(self, old_version, target_version):
        if not old_version:
            logger.error(
                f"Please provide the old version of {self.package_name}."
            )
        else:
            self.old_version = old_version

        if not target_version:
            # Get the current version of the package from the env
            try:
                result = subprocess.run(
                    ["pip", "show", self.package_name],
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
                    f"Error: Could not determine the current version of {self.package_name}."
                )
                self.target_version = None
        else:
            self.target_version = target_version

    def detect_package_usage(self):

        self.usage_detector = PackageUsageDetector(self.repo_path, self.package_name)
        self.usage_detector.run()
        self.usage_results = self.usage_detector.results

        return self.usage_results

    def get_usage_summary(self):
        """
        Generate a summary of package usage.
        """
        if not self.usage_results:
            self.detect_package_usage()

        return self.usage_results

    def run(self):
        """
        Run the migration process
        """
        self.detect_package_usage()
        self.get_usage_summary()
        return self.usage_results


if __name__ == "__main__":
    migrator = PackageMigrator(repo_path="test_cases/current").run()
