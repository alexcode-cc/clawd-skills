# ntopng Admin Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ntopng](https://img.shields.io/badge/ntopng-6.4+-orange.svg)](https://www.ntop.org/products/traffic-analysis/ntop/)

> ⚠️ **WARNING: This tool grants HIGH PRIVILEGE access to your network.**
> By using it, you declare you are a responsible adult. [See full disclaimer](SKILL.md)

Network traffic monitoring and analysis for AI agents using ntopng.

## 🚀 Quick Start

```bash
# Clone the skill
gh repo clone Transcendenceia/ntopng-admin-skill

# Configure credentials
export NTOP_URL="https://ntopng.yourdomain.com"
export NTOP_USER="admin"
export NTOP_PASS="your_password"

# Check status
./scripts/ntopng-helper.sh status

# View active flows
./scripts/ntopng-helper.sh flows
```

## 📋 Features

- **📊 Real-time Flow Analysis** - Active connections and data usage
- **🖥️ Host Monitoring** - Top bandwidth consumers
- **🚨 Security Alerts** - Network-level security alerts
- **📈 Traffic Reporting** - Security audit data extraction
- **🔍 Network Discovery** - Detect new devices and anomalies

## 📖 Documentation

See [SKILL.md](SKILL.md) for complete documentation.

## 🔧 Requirements

- ntopng 6.4+ (Community or Professional)
- curl and jq installed
- Valid ntopng credentials

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

## 🤝 Contributing

Contributions welcome! Please open issues and pull requests.

## ⚠️ Disclaimer

This is an unofficial skill. Not affiliated with the ntopng project or ntop.org.
