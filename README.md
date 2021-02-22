# ELSA Localization Pipeline

Easy Localization System Access (ELSA) is a modular continuous translation and localization system that ensures all content published on connected Content Management Systems (CMS) is automatically and continuously kept up to date in any number of specified languages, using a combination of Neural Machine Translation (NMT) and human Localization vendors.

This Proof of Concept codebase was built by NYCx Innovation Fellows working with the Mayor’s Office of the CTO (MOCTO)to explore streamlining the process of translation management for itself and potentially other city agencies. It is provided as-is.

**Please reach out to [jiman@cto.nyc.gov](mailto:jiman@cto.nyc.gov) if you would like to get involved!**

## Getting Started

To get ELSA set up and running, see the [Getting Started](https://github.com/nyc-cto/tms/blob/master/docs/getting-started.md)


## Background
The primary objective of Project ELSA was to explore and provide a low level, zero-interface pipeline for automatically ensuring that all digital content produced by an NYC agency could be kept in sync across multiple lanugages, reduce time-to-live on multilingual content, and reduce duplicative string translations where possible, while minimizing staff time overhead.

### Goals
- Modular to maintain flexibility and allow a plugin architecture
- Fully asynchronous and queue based to maximize low-cost infrastructure
- Zero-interface because ELSA should be fully transparent to a content creator/editor
- Built in Translation Memory to ensure that common strings aren't re-translated repeatedly
- Designed for the needs of government

### Non-Goals
- Not a commercial product so it does not fit every need or every edge case - if it doesn't fit your usecase, please consider [contributing](/CONTRIBUTING.md)
- Not a project management tool for translation workflows - there are other tools out there that do that well
- Not a CAT tool - translation and localization is done outside of ELSA, this is just the pipeline.
- Not right the first time - we believe in iterative work and understand we will get it wrong. If you see somewhere we could improve, please submit an issue

## Contributors
Many thanks to the following individuals who have made significant contributions to this project:
- [Steve Young](https://github.com/liquidsteves)
- [Matt Silver](https://github.com/matthewsilver)
- [Rapi Castillo](https://github.com/nyccto-rapicastillo)
- [Shannon Ladymon](https://github.com/sladymon)
- [Aditya Sridhar](https://github.com/as1729)
- [Alex Chen](https://github.com/chena11356)
- [Justin Isaf Man](https://github.com/jisaf)

## License
See [LICENSE](/LICENSE)
