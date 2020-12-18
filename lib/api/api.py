import re
import requests
import toml


class Canvas:
    def __init__(self, config_file: str):
        """Interface to Canvas API."""
        self.cfg: dict = toml.load(config_file)
        # self.token = self.get_access_token()
        self.token: str = self.cfg['secret']['manual_token']
        self.version: str = 'v1'
        self.base_url: str = self._get_base_url()
        self.std_headers: dict = self._get_std_headers()

    def get_access_token(self):
        """TODO: to be implemented"""
        pass

    def get_courses(self) -> list:
        """Returns a list of all of the student's courses."""
        res: object = requests.get(
            f'{self.base_url}/{self.version}/courses',
            headers=self.std_headers
        )
        return self._get_all_pages(res)

    def get_assignments_in_course(self, course_id: int, params=None) -> list:
        """Returns a list of all the assignments in the course."""
        if params is None:  # default parameters if params isn't passed
            params: dict = {
                'include': ['submission'],  # includes score
                'order_by': 'due_at',
            }
        res: object = requests.get(
            f'{self.base_url}/{self.version}/courses/{course_id}/assignments',
            params=params,
            headers=self.std_headers
        )
        return self._get_all_pages(res)

    def get_assignment_groups_in_course(self, course_id: int) -> list:
        """Returns a list of all the assignment groups in the course."""
        res: object = requests.get(
            f'{self.base_url}/{self.version}/courses/{course_id}/assignment_groups',
            headers=self.std_headers
        )
        return self._get_all_pages(res)

    def get_grading_standard_in_course(self, course_id: int) -> list:
        """Returns a list of all the grading standards in the course."""
        res: object = requests.get(
            f'{self.base_url}/{self.version}/courses/{course_id}/grading_standards',
            headers=self.std_headers
        )
        # There's only one page for this.
        return res.json()

    def _get_base_url(self) -> str:
        """Returns the base url to be used in API requests."""
        proto: str = self.cfg['canvas']['protocol']
        url: str = self.cfg['canvas']['url']
        return f'{proto}://{url}/api'

    def _get_std_headers(self) -> dict:
        """Returns the standard headers to be used for most API requests."""
        return {'Authorization': f'Bearer {self.token}'}

    def _get_all_pages(self, res: object) -> list:
        """Returns a list consisting of data from all the pages.

        The Canvas API only returns a default of 10 items per page. Links
        to other pages are in the response header.
        """
        data: list = res.json()
        # Keep adding to the list of data while there is a next page.
        while True:
            try:
                next_url: str = re.search(
                    '<([^>]+)>; rel="next"', res.headers['Link']).group(1)
                res = requests.get(next_url, headers=self.std_headers)
                data += res.json()
            except AttributeError:
                break  # next page not found
        return data
