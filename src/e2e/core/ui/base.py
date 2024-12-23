import typing as t

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from e2e.core.logger import logger

E = t.TypeVar('E', bound='Element')


class ElementCallable(t.Generic[E]):
    def __init__(
        self,
        wd: WebDriver,
        dtype: t.Type[E],
        failable=False,
    ) -> None:
        self.wd = wd
        self.dtype: t.Type[E] = dtype
        self.failable = failable

    def __call__(
        self,
        access_id: str | None = None,
        ios_access_id: str | None = None,
        adr_access_id: str | None = None,
        xpath: str | None = None,
        ios_xpath: str | None = None,
        adr_xpath: str | None = None,
        timeout: float | None = None,
        poll_frequency: float | None = None,
        **kwargs,
    ) -> E:
        return self.dtype(
            wd=self.wd,
            access_id=access_id,
            ios_access_id=ios_access_id,
            adr_access_id=adr_access_id,
            xpath=xpath,
            ios_xpath=ios_xpath,
            adr_xpath=adr_xpath,
            timeout=timeout,
            poll_frequency=poll_frequency,
            failable=self.failable,
            **kwargs,
        )


class Element(WebElement):
    def __init__(self, **kwargs) -> None:
        self.wd: WebDriver | None = kwargs.get('wd')
        self._element: WebElement | None = kwargs.get('_element')
        self.access_id: str | None = kwargs.get('access_id')
        self.ios_access_id: str | None = kwargs.get('ios_access_id')
        self.adr_access_id: str | None = kwargs.get('adr_access_id')
        self.xpath: str | None = kwargs.get('xpath')
        self.ios_xpath: str | None = kwargs.get('ios_xpath')
        self.adr_xpath: str | None = kwargs.get('adr_xpath')
        self.failable: bool = kwargs.get('failable', False)
        self.timeout: float = kwargs.get('timeout') or 8
        self.poll_frequency = kwargs.get('poll_frequency') or 0

    def _make_locator(self) -> t.Tuple[AppiumBy, str]:
        def first_match(*xs) -> t.Tuple[AppiumBy, str]:
            return next(x for x in xs if x[1])

        platform = self.wd.capabilities['platformName']
        if platform == 'iOS':
            return first_match(
                (AppiumBy.ID, self.access_id),
                (AppiumBy.ID, self.ios_access_id),
                (AppiumBy.XPATH, self.xpath),
                (AppiumBy.XPATH, self.ios_xpath),
            )
        if platform == 'Android':
            return first_match(
                (AppiumBy.ID, self.access_id),
                (AppiumBy.ID, self.adr_access_id),
                (AppiumBy.XPATH, self.xpath),
                (AppiumBy.XPATH, self.adr_xpath),
            )
        raise RuntimeError(f'Unsupported platform: {platform}')

    def _evaluate(
        self: E,
        availability: bool = True,
    ) -> E:
        if self._element:
            return self

        locator = self._make_locator()
        wd_wait = WebDriverWait(
            self.wd,
            timeout=self.timeout,
            poll_frequency=self.poll_frequency,
        )
        try:
            if availability:
                ec = EC.presence_of_element_located(locator)
            else:
                ec = EC.invisibility_of_element_located(locator)
            wd_wait.until(ec)
            self._element = self.wd.find_element(locator[0], locator[1])
            self.__dict__.update(self._element.__dict__)
        except Exception as e:
            if self.failable:
                return self
            # If expected not to see the element, the type would be NoSuchElementException
            if not availability and isinstance(e, NoSuchElementException):
                return self
            if availability:
                msg = f'Could not find element with locator {locator}'
            else:
                msg = f'Element with locator {locator} still exists'
            logger.error(msg)
            raise AssertionError(msg) from None
        return self

    def tap(self):
        self.must_exist().click()

    def must_exist(self: E) -> E:
        return self._evaluate()

    def must_not_exist(self):
        self._evaluate(availability=False)

    @property
    def exists(self) -> bool:
        return self._element is not None
