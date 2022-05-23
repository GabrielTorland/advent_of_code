import sys, os, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class GetInput:
    def __init__(self) -> None:
        self.driver = self.create_driver()
        self.login()

    def create_driver(self) -> webdriver:
        """
        Creates a webdriver and returns it
        """        
        options = Options()
        options.add_argument("--headless")
        # If you already have a chromedriver.exe, change this to your own path
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(10)
        return driver

    def login(self) -> None:
        """
        Logs in to your advent of code account via github
        """        
        # Change to your own path to login info
        file = os.path.abspath("/Users/MSI Gaming PC/github/credentials.json")
        credentials = json.load(open(file))
        self.driver.get("https://github.com/login?client_id=7bb0a7ec13388aa67963&return_to=%2Flogin%2Foauth%2Fauthorize%3Fclient_id%3D7bb0a7ec13388aa67963%26duration%3Dtemporary%26redirect_uri%3Dhttps%253A%252F%252Fadventofcode.com%252Fauth%252Fgithub%252Fcallback%26response_type%3Dcode%26scope%3D%26state%3Dx")
        self.driver.find_element_by_id("login_field").send_keys(credentials["username"])
        self.driver.find_element_by_id("password").send_keys(credentials["password"])
        self.driver.find_element_by_name("commit").click()
    
    def write_input_to_file(self, day, year):
        """Writes the input to .in file.
        Args:
            day (str): What day of the advent of code challenge
            year (str): What year the advent of code challenge is in
        """        
        self.driver.get(f"https://adventofcode.com/{year}/day/{day}/input")

        # change this to your own path
        file = os.path.abspath(f"/Users/MSI Gaming PC/advent_of_code/{year}/day_{day}/input.in")
        with open(file, 'w') as f:
            test = self.driver.find_element_by_xpath("/html/body/pre").text
            f.writelines(test)

if __name__ == "__main__":
    assert len(sys.argv) == 3
    # User input
    day, year = sys.argv[1], sys.argv[2]
    get_input = GetInput()
    get_input.write_input_to_file(day, year)

