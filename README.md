# BigscreenVR.com – MTA-STS Policy

## What is this?

This repository exists solely to host the **MTA-STS policy file** for the domain:

```
https://mta-sts.bigscreenvr.com/.well-known/mta-sts.txt
```

MTA-STS (Mail Transfer Agent Strict Transport Security) is a modern email security standard.  
It tells other mail servers that when they send mail *to* `@bigscreenvr.com`, they must use **TLS encryption** and validate our MX records, rather than falling back to insecure delivery.

By publishing this policy, we protect inbound mail from:
- **Downgrade attacks** (attackers forcing mail to be delivered without TLS).  
- **MX spoofing** (attackers redirecting mail to a rogue server).  

---

## Current Policy

The current MTA-STS policy is configured in `.well-known/mta-sts.txt`:

```txt
version: STSv1
mode: testing
mx: *.google.com
max_age: 86400
```

### Policy Details

- **Version**: STSv1 (current standard)
- **Mode**: Testing (allows fallback to non-TLS if needed)
- **MX Records**: Accepts any subdomain of google.com
- **Max Age**: 86400 seconds (24 hours)

## Implementation

### DNS Configuration

To enable MTA-STS, you need:

1. **CNAME Record**: `mta-sts.bigscreenvr.com` → `bigscreenvr.com`
2. **Policy File**: Available at `https://mta-sts.bigscreenvr.com/.well-known/mta-sts.txt`

### Web Server Configuration

The policy file must be served with:
- **Content-Type**: `text/plain`
- **HTTPS**: Required (no HTTP fallback)
- **Access**: Publicly accessible

---

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Access to the bs-pre organization on GitHub

### Quick Setup

Run the setup script to configure your development environment:

```bash
./scripts/setup-dev.sh
```

This script will:
- Install Python dependencies
- Set up git hooks for policy validation
- Configure the development environment
- Run tests to verify everything works

### Manual Setup

If you prefer to set up manually:

1. **Clone the repository**:
   ```bash
   git clone git@github.com:bs-pre/mta-sts-policy.git
   cd mta-sts-policy
   ```

2. **Set up Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install git hooks**:
   ```bash
   cp scripts/pre-commit .git/hooks/
   chmod +x .git/hooks/pre-commit
   ```

4. **Verify setup**:
   ```bash
   python3 scripts/validate-policy.py
   ```

### Git Hooks

The repository includes pre-commit hooks that automatically validate the MTA-STS policy before allowing commits. This ensures:

- Policy syntax is correct
- Required fields are present
- Values are within valid ranges
- No invalid policies can be committed

---

## Validation

### Local Validation

Validate the policy locally before committing:

```bash
python3 scripts/validate-policy.py
```

### CI/CD Validation

The GitHub workflow automatically validates the policy on:
- Every push to main/develop branches
- Every pull request to main
- Policy file changes trigger validation

### Validation Rules

The policy must contain:
- `version: STSv1`
- `mode: testing` or `mode: enforce`
- `mx: <mx-pattern>` (supports wildcards)
- `max_age: <seconds>` (300-86400)

---

## Deployment

### Testing Mode

Currently set to `mode: testing` which:
- Allows fallback to non-TLS delivery
- Logs policy violations
- Safe for initial deployment

### Production Mode

To enable strict enforcement:
1. Change `mode: testing` to `mode: enforce`
2. Test thoroughly in staging
3. Monitor mail delivery
4. Deploy to production

---

## Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/description`
3. **Make your changes**
4. **Test locally**: `python3 scripts/validate-policy.py`
5. **Commit with validation**: Git hooks will validate automatically
6. **Push and create a pull request**

### Code Style

- Follow PEP 8 for Python code
- Use descriptive commit messages
- Include tests for new functionality
- Update documentation as needed

---

## Security

### Policy Validation

- All policy changes are validated before commit
- CI/CD ensures policy compliance
- Automated testing prevents invalid policies

### Access Control

- Repository is private
- Only authorized contributors can modify policies
- All changes require pull request review

---

## Troubleshooting

### Common Issues

1. **Policy validation fails**:
   - Check syntax in `.well-known/mta-sts.txt`
   - Ensure all required fields are present
   - Verify field values are within valid ranges

2. **Git hooks not working**:
   - Ensure hooks are executable: `chmod +x .git/hooks/pre-commit`
   - Check Python path in hook script
   - Verify validation script exists

3. **CI/CD failures**:
   - Check GitHub Actions logs
   - Verify policy file syntax
   - Ensure all required fields are present

### Getting Help

- Check the GitHub Issues page
- Review the validation script output
- Consult MTA-STS documentation
- Contact the development team

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Resources

- [MTA-STS RFC 8461](https://tools.ietf.org/html/rfc8461)
- [GitHub MTA-STS Documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-an-apex-domain)
- [Email Security Best Practices](https://www.ietf.org/blog/mta-sts/)
