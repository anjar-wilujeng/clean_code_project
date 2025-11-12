# Clean Code Project - SonarQube Example

Project Python sederhana dengan kualitas kode tinggi untuk testing SonarQube.

## Fitur

- User registration system
- User authentication
- SQLite database integration
- Comprehensive error handling
- Full unit test coverage
- Clean code practices

## Struktur Project

```
clean_code_project/
├── app.py                      # Main application code
├── test_app.py                 # Unit tests
├── requirements.txt            # Project dependencies
├── sonar-project.properties    # SonarQube configuration
└── README.md                   # Project documentation
```

## Kualitas Kode

Project ini didesain dengan best practices berikut:

### Security (A Rating)
- Password hashing menggunakan SHA-256
- SQL injection prevention dengan parameterized queries
- Input validation untuk semua user inputs
- Proper error handling dengan custom exceptions

### Reliability (A Rating)
- Comprehensive exception handling
- Type hints untuk semua functions
- Proper resource management (database connections)
- No unused variables or parameters
- All code paths properly tested

### Maintainability (A Rating)
- Clear and descriptive naming conventions
- Comprehensive docstrings untuk semua functions
- Constants defined untuk magic strings
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)
- Proper code organization

### Code Coverage
- 100% function coverage
- Comprehensive unit tests
- Edge cases tested
- Error conditions tested

## Setup dan Running

### 1. Menjalankan Aplikasi

```bash
python app.py
```

### 2. Menjalankan Unit Tests

```bash
python -m unittest test_app.py -v
```

### 3. SonarQube Analysis

#### Prerequisite
- SonarQube Server running (default: http://localhost:9000)
- SonarScanner installed

#### Jalankan Analysis

```bash
# Menggunakan SonarScanner
sonar-scanner \
  -Dsonar.projectKey=clean-code-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN
```

Atau jika sudah ada file `sonar-project.properties`:

```bash
sonar-scanner
```

## Best Practices yang Diterapkan

1. **No Code Smells**
   - Tidak ada duplikasi kode
   - Tidak ada unused variables/parameters
   - Tidak ada magic numbers/strings
   - Exception handling yang spesifik

2. **Security Best Practices**
   - Password tidak disimpan dalam plain text
   - SQL injection prevention
   - Input validation
   - Proper error messages (tidak expose sensitive info)

3. **Clean Code Principles**
   - Readable and self-documenting code
   - Proper naming conventions
   - Single Responsibility Principle
   - SOLID principles
   - Comprehensive documentation

4. **Testing**
   - Unit tests untuk semua functionalities
   - Test coverage untuk happy path dan edge cases
   - Isolated test environment
   - Proper setup and teardown

## Expected SonarQube Results

Dengan kode ini, Anda seharusnya mendapatkan:

- **Security Rating**: A (No vulnerabilities)
- **Reliability Rating**: A (No bugs)
- **Maintainability Rating**: A (Low technical debt)
- **Coverage**: 90%+ (dengan unit tests)
- **Duplications**: 0%
- **Code Smells**: 0 atau sangat minimal

## Catatan

Project ini adalah contoh untuk demonstrasi. Dalam production environment:
- Gunakan hashing algorithm yang lebih kuat (bcrypt, argon2)
- Implementasi proper authentication system (JWT, sessions)
- Tambahkan logging
- Implementasi rate limiting
- Gunakan environment variables untuk konfigurasi
- Tambahkan integration tests

## Lisensi

MIT License - Free to use for educational purposes
