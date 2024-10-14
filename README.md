<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->

[![PyPI - Version][pypi-version-shields]][pypi-url]
[![PyPI - Python Version][pypi-python-versions-shields]][pypi-url]
[![Downloads](https://static.pepy.tech/badge/post-tracker)][pypi-url]

<!--[![Contributors][contributors-shield]][contributors-url]-->
<!-- [![Forks][forks-shield]][forks-url]-->

<!-- [![Tests][tests-shield]][github-repo-url] -->
[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->

<br />

<div align="center">

  <h2 align="center">Post Tracker</h2>

  <p align="center">
A command-line tool to get information about parcel's tracking from https://tracking.post.ir
  </p>

  <a href="https://github.com/amiraref/post-tracker/issues">Report Bug</a>
  ·
  <a href="https://github.com/amiraref/post-tracker/issues">Request Feature</a>


  <br/>

  <a href="#">
      <img src="https://raw.githubusercontent.com/amiraref/post-tracker/master/images/output-2.png?raw=true" alt="Screenshot" height="500" style="border-radius: 5px;">
  </a>

</div>



## Install the program :
install the post-tracker using pip :
```bash
pip install post-tracker
```

<br/>

## Using as a library
To use the `post_tracker` as a library in your projects, do as following :

```python
import asyncio
from post_tracker import PostTracker
from post_tracker.errors import TrackingNotFoundError

async def main():
    code = "12345" # tracking code
    async with PostTracker() as tracker_app:
        try:
            # get tracking data
            result = await tracker_app.get_tracking_post(tracking_code=code)
            print(result)
        except TrackingNotFoundError as e:
            # tracking data not found
            return print(e)


asyncio.run(main())
```

<br/>


## Using as a CLI tool
After install, just write `post-tracker` command to access to program :
```bash
# get help
post-tracker -h
# or, pass your tracking code
post-tracker -c 123456789101111213
```

<br/>

## Telegram Bot:
there is also a telegram robot developed based on this library to get parcel's tracking information in **telegram**:

[Repository](https://github.com/amirAref/post-tracker-bot)
.
[Robot](https://t.me/IRPostTrackerbot)


<br/>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Here is the [Contributing Guidelines](https://github.com/amiraref/post-tracker/blob/master/CONTRIBUTING.md).
Don't forget to give the project a star! Thanks again!

<br/>

<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/amiraref/post-tracker/blob/master/LICENSE) for more information.

<br/>
<!-- TODO-->

## TODO:
- [x] create models to better parsing the data.
- [x] create dmenu (or fzf menu) to save tracking codes in local cache and select in future program's runs.
- [x] add installer script as a CLI tool in linux machines.
- [x] create [python telegram bot](https://github.com/amiraref/post-tracker-bot).
- [x] make output result prettiy.
- [x] make and test compatibily with windows os
- [x] publish on pypi.org
- [ ] write README.md in persian
- [ ] re-write cli using click library
- [ ] write tests
- [ ] add CI/CD




<!-- MARKDOWN LINKS & IMAGES -->
<!-- SHIELDS -->
[contributors-shield]: https://img.shields.io/github/contributors/amiraref/post-tracker.svg?style=for-the-badge
[forks-shield]: https://img.shields.io/github/forks/amiraref/post-tracker.svg?style=for-the-badge
[stars-shield]: https://img.shields.io/github/stars/amiraref/post-tracker?style=flat&color=green
[issues-shield]: https://img.shields.io/github/issues/amiraref/post-tracker.svg
[license-shield]: https://img.shields.io/github/license/amiraref/post-tracker.svg
<!-- other links -->
[contributors-url]: https://github.com/amiraref/post-tracker/graphs/contributors
[forks-url]: https://github.com/amiraref/post-tracker/network/members
[stars-url]: https://github.com/amiraref/post-tracker/stargazers
[issues-url]: https://github.com/amiraref/post-tracker/issues
[license-url]: https://github.com/amiraref/post-tracker/blob/master/LICENSE
[pypi-url]: https://pypi.org/project/post-tracker
[github-repo-url]: https://github.com/amiraref/post-tracker

<!-- [product-screenshot]: images/screenshot.png -->

[Pydantic.badge]: https://img.shields.io/badge/pydantic-black?style=for-the-badge&logo=pydantic&logoColor=red
[Httpx.badge]: https://img.shields.io/badge/Httpx-gray?style=for-the-badge
[tests-shield]: https://github.com/amiraref/post-tracker/actions/workflows/tests.yml/badge.svg
[pypi-version-shields]: https://img.shields.io/pypi/v/post-tracker
[pypi-python-versions-shields]: https://img.shields.io/pypi/pyversions/post-tracker
