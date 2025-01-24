# Config

- [x] Set up postgres and .env

# Auth, Signup, Login

- [ ] Use JWTs and roles (dentist, supervisor, patient)
- [ ] Username would be phone number (for patients)
- [ ] supervisors and dentist creds will be in different table??
- [ ] Dentist, supervisor permissions:
  - [ ] change any patient's phonenumbers
  - [ ] add patients (full form, fire 2 queries: password table and details table)
- [ ] Dentist permissions:
  - [ ] Add supervisors
- [ ] Patients permissions:
  - [ ] change their own phonenumbers
  - [ ] change their own passwords
- [ ] passwords hashed with bcrypt
