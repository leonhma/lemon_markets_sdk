# contributing

Contributions are welcome!
If you discover bugs or have ideas to make this SDK easier to use, feel free to fork this repo, work on your changes, and open a pull request.

## Rules

* You should tell us what you changed in this pull request to make it easier for us to understant you code.
* If this pull request is the answer to an open issue, please link to it.
* Every time presented to the user should be timezone aware and localized to their timezone. This is to avoid confusion and make sure that the user understands what time it is. See [Tips](#Tips) for helper functions to help with timezones.

## Tips

* The `lemon_markets.helpers.time_helper` module helps tremendously with parsing timestamps and working with timezone-aware datetimes.
