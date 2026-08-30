# Changelog

## 1.0.18

- Add optional Home Assistant settings for overriding charging and discharging efficiency values.

## 1.0.17

- Replace `export_to_grid` with `discharge_to_grid` in optimizer requests.
- Forward end-to-end incoming request headers to the optimizer.
- Add Home Assistant changelog metadata and release workflow validation.
- Add pytest coverage and Visual Studio Code Testing integration.
- Standardize local test execution on a project-local virtual environment.

## 1.0.16

- Forward optimizer API paths below `/proxy` to the configured optimizer URL.
- Forward end-to-end request headers, including authorization tokens.
- Load the configured log level from Home Assistant options.
- Persist runtime configuration changes in Home Assistant options.
- Restore `https://optimizer.evcc.io` as the default optimizer URL.
