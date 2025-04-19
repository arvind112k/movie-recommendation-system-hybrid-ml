from setuptools import setup, find_packages

from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if "-e ." in requirements:
            requirements.remove("-e .")

    return requirements


setup(
    name="movie_recommendation_system",
    version="0.1.0",
    author="Arvind Kumar",
    author_email="arvind112k@gmail.com",
    description="Movie Recommendation System using Machine Learning",
    long_description="This is a movie recommendation system built using machine learning techniques. It provides personalized movie recommendations based on user preferences and behavior.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),




)