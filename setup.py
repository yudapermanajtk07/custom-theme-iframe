from setuptools import setup, find_packages

setup(
    name='custom-theme-iframe',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        "lms.djangoapp": [
            "custom_theme_iframe = custom_theme_iframe.apps:CustomThemeIframeConfig",
        ],
    },
)
