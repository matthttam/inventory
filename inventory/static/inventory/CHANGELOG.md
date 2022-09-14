# Changelog


## (unreleased)

### Changes

* Improved UI. [Matt henry]

### Fix

* Table rows properly vertically align as expected. [Matt henry]

### Other

* Vscode settings. [Matt henry]

* Fixed test by using an explicit append. [Matt Henry]

* Fixing tests. [Matt henry]

* Writing tests for dashboard. [Matt henry]

* Fixing tests. [Matt henry]

* Remove unused features such as omni search and Activity Log link. [Matt henry]

* Fix gitignore to not ignore all static files. [Matt henry]

* Remove old dashboard. [Matt henry]

* Fix regression of Quick Assign button on dashboard appearing for users with no rights. [Matt henry]

* Removed some spacing. [Matt henry]

* Initial updates to dashboard UI. [Matt henry]


## 1.3.1 (2022-08-21)

### Other

* Updated CHANGELOG. [Matt Henry]

* Fixed(google): Corrected a glitch that would incorrectly update locations for devices every other run of update_google_devices. [Matt Henry]

* Fixed(google): Corrected a glitch that would incorrectly update locations for devices every other run of update_google_devices. [Matt Henry]

* Changed: Disabled batch functionality for chromeosdevice service. [Matt Henry]

  Batch functionality is triggering rate limits

* Fixed: Missing dependency for gunicorn. [Matt Henry]


## 1.3.0 (2022-08-20)

### Other

* Create a basic changelog. [Matt Henry]

* Added(chore): Implemented keep-a-changelog and git-chglog. [Matt Henry]

* Added django-selenium-login to requirements file. [Matt Henry]

* Added column visibility options and state saving. [Matt henry]

* Change to using SHORT_DATETIME_FORMAT so it works across other languages. Clean up view. [Matt henry]

* Fix display of date and time in detail view of assignments. [Matt henry]

* Wrote tests for quick assign and corrected search behavior. [Matt henry]

* Working on testing quick assign. [Matt henry]

* Fixed a typo. [Matt henry]

* Removed debug code leftover from other commit. [Matt henry]

* Fix some bugs and write tests for update_google_devices. [Matt henry]

* Revert back to using just one requirements file. Multiples really aren't needed. Removed playwright as a requirement. Updated djangot to 4.0.7. [Matt henry]

* Removed use of playwright. We don't want to have this installed on our server since we are switching to selenium. [Matt henry]

* Fix tests and removed commented code. [Matt henry]

* Implemented a command to update the location field of all devices in google if needed. [Matt henry]

* Stuff. [Matt Henry]

* Tested that the device search box is focused on initial page load! [Matt Henry]

* Changed from using playwright to selenium now that I have selenium working faster! [Matt Henry]

* Helper function to retrieve a chrome driver for testing. helper function for setting a value of an element. [Matt Henry]

* Selenium may be working! [Matt Henry]

* Remove the quick assign button if the user does not have permisisons. Updated tests. [Matt Henry]


## 1.2.1 (2022-08-14)

### Other

* Properly ignore public/static/ and config/ [matthttam]

* Still trying to ignore pulic/static... [matthttam]

* Ignore static files. [matthttam]

* Added a bash script to run commands under the python/django environment. [matthttam]

* Updating settings to pull CSRF_TRUSTED_ORIGINS. [matthttam]

* Updating sample environment. [matthttam]


## 1.2 (2022-08-10)

### Other

* Make dashboard have a GIANT quick assign button. [Matt henry]

* Fix a bug where history was being improperly rendered on all pages. [matthttam]

* Fix a bug in admin that caused 500 errors on searching some admin sections. [matthttam]

* Fixed a bug where we passed the wrong device ID to move devices. [Matt henry]

* Rewrote google update triggers for assignments to include unassigned. [Matt henry]

* Fixed tests. [Matt henry]

* Fix mising DB constraints. Fix class names in admin. [matthttam]

* Fix the run_command script to work within cron. [matthttam]

* Fix admin view and corrected dashboard nav tests. [Matt henry]

* Correct a test regarding a previous model change on Devices. [Matt henry]

* Fix a bug that prevented staff from seeing the admin dropdown. [Matt henry]

* Fix a bug that prevented multiple blanke assetIDs for devices. [Matt henry]

* Removed has_outstanding_assignment in favor of is_currently_assigned to correct a bug. [Matt henry]

* Fixed missing search box for GoogleDeviceAdmin. [Matt henry]

* Fixed a bug that could prevent a device from moving in google when it is supposed to. [Matt henry]

* Fixed a display bug where the dropdown would not move properly after a message in quick assign. Fixed a bug wehre the button would not focus after auto selecting. [Matt henry]

* Fixed display of person_type in DeviceBuildingToGoogleOUMappings. [Matt henry]

* Fix a bug where an error occurring would allow for duplicate assignments. [Matt henry]

* Fixed a bug that would cause an error when moving a device triggers from an assignment. [Matt henry]

* Fix tests. [Matt Henry]

* Fixing bugs and improving sync commands. [Matt Henry]

* Refactored all detail, delete, and turnin views by abstracting the infobox. [Matt Henry]

* Refactoring templates. [Matt Henry]

* Removed old code. [Matt Henry]

* Button updates. [Matt henry]

* Remove commented code. [Matt henry]

* Fix some major bugs regarding timestamps. Implemented a turnin button. [Matt Henry]

* Trying to make things work. [Matt henry]

* Clean up dev to fix some tests and work with mysql from now on instead of sqlite. [Matt henry]


## 1.1.1 (2022-08-05)

### Other

* Fix bugs with device sync. [Matt henry]

* Added the run_command script for production. Updated gitignore for production. [matthttam]


## 1.1 (2022-08-04)

### Other

* Fix cosmetic issue for profile. [Matt henry]

* Remove use of GroupConcat as it is not working. [Matt henry]

* Trying to fix migrations. [Matt henry]

* Trying to fix migrations for mysql. [Matt henry]

* Temporary fix. [Matt henry]

* Working on fixing stuff. [Matt henry]

* Working on fixing stuff. [Matt henry]

* Revereted. [Matt henry]

* Again. [Matt henry]

* Trying to fix a migration. [Matt henry]

* Hopefully fix a bug with mysql aggregates. [Matt henry]

* Sudo code. [Matt Henry]

* Added person_type to the Building to OU device mapping. Updated the device_assignment_actions to do all the things. [Matt Henry]

* Moved functionality to the assignment update itself. [Matt Henry]

* Made it so that changing the building of a device runs a command to move the device OU. [Matt henry]

* Began working on move command. [Matt henry]

* Made signal receivers to change device building upon assignment and trigger when device is saved if the mapped building ou doesn't match the device's google_device ou. [Matt henry]

* Fixed a test. [Matt henry]

* Fixed tests and added placeholders. [Matt henry]

* Fixed tests. [Matt henry]

* More testing. [Matt henry]

* Fixed model tests. [Matt henry]

* Fix more tests. [Matt Henry]

* Working on fixing tests and updated factories. [Matt Henry]

* Fixed more tests. [Matt henry]

* Fixed several tests. MappingAbstract has issues though. [Matt henry]

* Finished feature and working on tests now. [Matt henry]

* Rewriting the device sync. [Matt henry]

* Person syncing working again using schema data. [Matt henry]

* Working. [Matt Henry]

* Working on fixing the from_field select options. [Matt Henry]

* Working on syncing google schema information into the DB to be used by the mappings, translations, and imports. [Matt Henry]

* Began work on storing person schema information which will allow typecasting as well as dropdown selection for mapping for google fields regardless of custom fields on a domain. [Matt Henry]

* Fix several tests. [Matt Henry]

* Writing tests. [Matt Henry]

* Testing utils. [Matt henry]

* Implemented logging and reworked templates for tables. [Matt henry]

* Fixed some bugs with the way people are syncing. [Matt henry]

* Refactored actions for datatables and applied them to Person and Devices. Fixed a bad test. [Matt henry]

* Improving quick assign. [Matt Henry]

* Fix tests for unique constraints. [Matt Henry]

* Fixed submit for quick assign. [Matt henry]

* Removed print statements from all tests. [Matt henry]

* Made quickassign submit work. [Matt henry]

* Got selectors working and fixed several basic bugs. Working on submit now. [Matt henry]

* Changed function based views into custom class based views. Created new Json Mixins. Cleaned up code for javascript. [Matt Henry]

* Fix mapping unique issue. [Matt henry]

* Update output. [Matt Henry]

* Updated tests and the way the quick assign works. [Matt Henry]

* Fix tests for base. [Matt Henry]

* Tons of changes to get quick assign working. Added extra parts to models to allow easier queries or filters. Fixed the bootstrap import to include its bundle. [Matt henry]

* Built quickassign. Built tests. [Matt Henry]

* Require auditlog and reorganized list. [Matt Henry]

* Fix cards to be the same height in the same row. [Matt henry]

* Fix test_infobox to properly look for content of each element. [Matt henry]

* Fixing tests. Organizing templates. [Matt henry]

* Removed old requirement. [Matt henry]

* Added BeautifulSoup4 to dev. [Matt henry]

* Reorganized and cleaned up code. [Matt Henry]

* Fixed several testing issues and UI problems. [Matt Henry]

* Upgraded the people module to work the same way as the others. Created tests for all items. [Matt Henry]

* Updated devices to use the same template structure as device assignments. Updated all tests to handle authenticaiton and permissions. [Matt Henry]

* Fix tests to match changes. [Matt Henry]

* Fix submit buttons. [Matt Henry]

* Tested base templates. [Matt Henry]

* Tested dashboard templates. [Matt Henry]

* Organize and test more templates. [Matt Henry]

* Fix tests except for devices. [Matt Henry]

* Corrected profile link and name. [Matt Henry]

* Added profiles urls to project. [Matt Henry]

* Implemented profiles properly. [Matt Henry]

* Finish testing assignment templates. [Matt Henry]

* Fix testing for partials and confirm delete. [Matt Henry]

* Trying to test infobox but having issues with dates. [Matt Henry]

* Working ont esting infobox. [Matt Henry]

* Cleaned up control buttons test. [Matt Henry]

* Cleaned up control buttons test. [Matt Henry]

* Correctly testing partials. [Matt Henry]

* Minor change. [Matt henry]

* Reworked templates for assignments. Began trying to test some templates for assignments. Updated assignments looks. [Matt Henry]

* Built out datatables and cleaned up device assignment templates. [Matt Henry]

* Safely pass information from django to be used by javascript to properly render the buttons for each row of the assignments table. [Matt Henry]

* Working on adding buttons based on user permission to the device assignment table. [Matt Henry]

* Rename assignment_list.js to deviceassignment_list.js. [Matt Henry]

* Deleted commented script and fixed formatting. [Matt Henry]

* Renamed url shortcut dashboard:index to dashboard:dashboard which is much clearer as to what it displays. [Matt Henry]

* Added permission check before rendinger new assignment button. [Matt Henry]

* Fixed nav issue where menu button didn't display after collapse. [Matt Henry]

* Updated assignment tests to handle permissions and implemented permission on several views and templates. [Matt Henry]

* Removed whitespace. [Matt henry]

* Removed comments. [Matt henry]

* Delete old module that has been created as a python package. [Matt henry]

* Remove console log. [Matt henry]

* Updated assignments view to include full name of user. Added permissions for detail page buttons. Created tests for detail page. Created tests for all assignment views including permissions. [Matt henry]

* Added a __str__ for DeviceAssignment model. [Matt henry]

* Using submodule as a real package now! [Matt Henry]

* Updated datatables for all three. Updated module. [Matt henry]

* Added playwright and querystring-parser to dev list. [Matt henry]

* Fix bad test. [Matt henry]

* Changes to submodule. [Matt Henry]

* Reworking datatables to use server side processing. [Matt Henry]

* Upgraded people views and set to server side processing (not complete) [Matt Henry]

* Added tests for permissions and updated login and other related views to look more modern. [Matt Henry]

* Fixed bad import. [Matt Henry]

* Break out requirements between different environments. [Matt Henry]

* Wrote additional tests. Need to refactor actual sync functions and break those out. Need to test link devices command. [Matt Henry]

* Move readme.md back to root. [Matt Henry]

* Created device link command which matches up devices to their google device counterpart by matching ids. [Matt henry]

* Removed accidental commen. [Matt henry]

* Simplify some code. [Matt henry]

* Fix device sync. Create link_google_devices command. Fix tests for google device sync. [Matt henry]

* Fixed testing for convert_google_user_to_person. Handle buildings and rooms using a hidden field. [Matt henry]

* Adding more tests. [Matt Henry]

* Refactoring sync_google_people and writing tests for the new functions. [Matt Henry]

* Fix url routs. [Matt Henry]

* Fixed lack of abstract in class Meta. [Matt Henry]

* Merged migrations between branches. [Matt Henry]

* Failed to save merged conflict file properly. [Matt Henry]

* Refactoring. [Matt Henry]

* Fix test. [Matt Henry]

* Wrote more tests. Refactored some code to make it easier to test. [Matt Henry]

* Removed commented code. [Matt Henry]

* Finished tests for models, Fixed views, added new requirements for testing. Altered field type for client email. [Matt Henry]

* Refactoring tests. [Matt henry]

* Tested GooglePersonTranslation. [Matt henry]

* More model tests. [Matt henry]

* Prtially wrote model tests. [Matt henry]

* Fixed name of field in model for googlesync. [Matt henry]

* Removed the credentials I accidentally uploaded! [Matt Henry]

* Update gitignore. [Matt Henry]

* Ignore secret files. [Matt Henry]

* Fixing tests. [Matt henry]

* Working on splitting out device model information. Created factories for googlesync. Began tests. [Matt henry]

* Fixing some bad migrations. Removed a bad init import file. Added a secret file to the ignore list. [Matt henry]

* Trying to fix the migration issues. [Matt henry]

* Device Sync Almost Working. Refactored all the google sync code. [Matt henry]

* Person sync working! [Matt henry]

* Almost done syncing people from google. [Matt henry]

* Added translations for google people. [Matt henry]

* Google Mapping. [Matt henry]

* Updated requirements for person model. [Matt henry]

* Partially implemented google person sync. [Matt henry]

* Start googlesyncapp. [Matt henry]

* Moved templates to a consistent folder to be used between development and production. Updated settings accordingly. [Matt Henry]

* Added a link to something if the user was a superuser. [Matt Henry]

* Created profiles to store timezone info. [Matt Henry]


## 1.0 (2022-07-14)

### Other

* Removed static files. [Matt Henry]

* Keep static folder even when empty. [dh_d59rp2]

* Ignore static files. [dh_d59rp2]

* Fix staging problems due to placing restart.txt in the wrong directory. Updated the settings file. [dh_d59rp2]

* Fixed formatting issue. [dh_d59rp2]

* Added timestamp formatting to logs. [dh_d59rp2]

* Fix tests for production staging. [Matt henry]

* Fix tests to be able to run on a database that is not recreated. [Matt henry]

* Testing providing the ID to factories. [Matt henry]

* Update settings to automatically create the log folder to prevent errors. [Matt henry]

* Fix a typo in sample environment. [Matt henry]

* Attempting to fix database queries in tests not working in MYSQL environment. [Matt Henry]

* Break out LOG_PATH into environment variable. [Matt Henry]

* Fix settings file to use env for allowed_hosts. [dh_d59rp2]

* Preparing for live deployment. [dh_d59rp2]

* Prepare for a released version. [dh_d59rp2]

* Updated settings and environment file. [Matt henry]

* Reconfigure settings to use environment file. [Matt henry]

* Building settings structure. [Matt henry]

* Updated .gitignore files. [Matt henry]

* Update gitignore to exclude sensitive files. [Matt Henry]

* Fix mistake of making is_inactive on wrong Model. [Matt Henry]

* Add is_active flag to device_type and people_type. [Matt Henry]

* Prevent secret file from being uploaded. [Matt henry]

* Asset_id now optional. Updated tests. [Matt henry]

* Update requirements. [Matt henry]

* Fixed all tests. Authentication is working! [Matt Henry]

* Created decorator to test for redirect to login. Updated device view tests. [Matt Henry]

* Testing for login and failed login. [Matt Henry]

* Added init.py to the dashboard app tests folder. [Matt Henry]

* Added namespace for audit even though views don't exist yet. [Matt Henry]

* Fix active tab for dashboard. [Matt Henry]

* Create custom login and logged_out templates and map urls. [Matt Henry]

* Finish tests. [Matt Henry]

* Almost finished all tests. [Matt Henry]

* Figured out L10N and basic date formatting so I can properly test for dates being passed. [Matt Henry]

* Partially tested DeviceAssignment Views. [Matt Henry]

* Fix assignment detail view and wrote tests for it. [Matt Henry]

* Form tests for assignments. [Matt Henry]

* More tests. [Matt Henry]

* More tests! Implemented DeviceAccessory model. [Matt Henry]

* Wrote some person tests. [Matt Henry]

* Update location models, tests, and factories. [Matt Henry]

* Make room number unique per building. [Matt Henry]

* Got rid of subproject faker_education. Finished model tests for devices. Changed some constraints on building models. [Matt Henry]

* Remove unused import. [Matt Henry]

* Tests for devices form. [Matt Henry]

* Formatting. [Matt Henry]

* Switch to using Black for formatting. [Matt Henry]

* Update workspace settings. [Matt Henry]

* Update requirements and delete old tests file. [Matt Henry]

* Several changes to fix some issues found during testing. [Matt Henry]

* Created devices tests and implemented other testing requirements like factory_boy and faker. [Matt Henry]

* Pytest config. [Matt Henry]

* Ignore vscode stuff. [Matt Henry]

* Create authentication app. [Matt Henry]

* Updated gitignore to ignore all of .vscode. [Matt Henry]

* Ignore .vscode folder. [Matt Henry]

* Created requirements file. [Matt henry]

* Remove ignored files. [Matt henry]

* Remove ignored files. [Matt henry]

* Using new gitignore. [Matt henry]

* Initial Commit. [Matt henry]


