XML Feature
======

** This is only a proposal and it may not reflect the final XML feature. **

For Tangra 3.0, the XML feature will be changed from the original one in Tangra 3.0. The design is now different.

- The stages should be stored externally (at least for now) and they will be required to use the public API to communicate with the server.
- When creating a study, you must create upload two files, separately. The first contains the user list, this will be used to generate the users. The second contains the study itself.
- If the users are already in the database, there is no need for the first file.
