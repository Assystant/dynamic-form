import setuptools

setuptools.setup(
    name="dynamic-form",
    version="0.0.16",
    author="Assystant",
    description="Custom form generation and submission management",
    install_requires=[
        "django",
        "djangorestframework",
        "django-extensions",
    ],
    url="https://github.com/Assystant/dynamic-form",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    # python_requires = ">=3.10"
)
