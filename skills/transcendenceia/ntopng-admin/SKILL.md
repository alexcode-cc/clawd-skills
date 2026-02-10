---
name: ntopng-admin
description: Monitor and analyze network traffic using ntopng. Use when you need to check real-time flows, identify top talkers on the network, analyze historical alerts, or troubleshoot connectivity issues. Supports ntopng 6.4 Community Edition and later.
---

# ntopng Admin

> ⚠️ **DISCLAIMER**
>
> This tool grants **HIGH PRIVILEGE** access to your network infrastructure.
> It can view sensitive traffic, plain-text credentials, and personal data.
>
> **By using this skill, you declare that:**
> - You are a responsible adult
> - You have authorization to monitor this network
> - You understand the security risks
> - You will use this tool ethically and legally
>
> **The author is not responsible** for misuse, unauthorized access, or damages
> resulting from the use of this skill.

Network traffic monitoring and analysis for AI agents using ntopng.

## Features

- 📊 **Real-time Flow Analysis** - View active connections and data usage
- 🖥️ **Host Monitoring** - Identify top bandwidth consumers
- 🚨 **Security Alerts** - Access network-level security alerts
- 📈 **Traffic Reporting** - Extract data for security audits
- 🔍 **Network Discovery** - Detect new devices and anomalies

## Installation

### Prerequisites

- ntopng 6.4+ (Community or Professional)
- curl and jq installed
- Valid ntopng credentials

### Quick Setup

1. Configure credentials via environment variables:
   ```bash
   export NTOP_URL="https://ntopng.yourdomain.com"
   export NTOP_USER="admin"
   export NTOP_PASS="your_password"
   ```

   Or create a credentials file:
   ```bash
   mkdir -p ~/.ntopng
   cat > ~/.ntopng/credentials << EOF
   NTOP_URL=https://ntopng.yourdomain.com
   NTOP_USER=admin
   NTOP_PASS=your_password
   EOF
   chmod 600 ~/.ntopng/credentials
   ```

## Usage

### Helper Script

```bash
# Get active flows
./scripts/ntopng-helper.sh flows

# List top hosts by bandwidth
./scripts/ntopng-helper.sh hosts

# View recent security alerts
./scripts/ntopng-helper.sh alerts

# Check if ntopng is online
./scripts/ntopng-helper.sh status
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/lua/get_flows_data.lua` | Active network flows |
| `/lua/get_hosts_data.lua` | Bandwidth usage by host |
| `/lua/get_alerts_data.lua` | Security alerts |
| `/lua/index.lua` | System status |

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NTOP_URL` | - | ntopng URL (required) |
| `NTOP_USER` | `admin` | Username |
| `NTOP_PASS` | - | Password (required) |
| `NTOP_INSECURE` | `false` | Set to `true` to disable SSL verification |

## Security Best Practices

1. **SSL Certificate Validation** - Enabled by default. Use `--insecure` or `NTOP_INSECURE=true` ONLY for development or self-signed certificates in internal networks
2. **Secure credentials** - Store passwords in environment variables or secure files (chmod 600)
3. **Limit access** - Create dedicated monitoring user if possible
4. **Regular audits** - Review alerts for suspicious traffic patterns

### SSL/TLS Configuration

By default, all connections validate SSL certificates. For production with valid certificates, no changes needed.

For self-signed certificates:
```bash
# Option 1: Command line flag
./scripts/ntopng-helper.sh --insecure flows

# Option 2: Environment variable
export NTOP_INSECURE=true
./scripts/ntopng-helper.sh flows
```

## Use Cases

### Network Security Audits
- Detect unknown MAC addresses
- Identify high-bandwidth usage from suspicious IPs
- Monitor traffic to restricted domains
- Find lateral movement patterns

### Performance Monitoring
- Identify bandwidth hogs
- Monitor application-specific traffic
- Track protocol distribution

### Troubleshooting
- Verify connectivity between hosts
- Check DNS resolution patterns
- Analyze dropped packets

## Version Compatibility

| ntopng Version | Skill Version | Status |
|----------------|---------------|--------|
| 6.4+ | 1.x | ✅ Supported |
| 6.0 - 6.3 | 1.x | ⚠️ May work |
| 5.x | 1.x | ❌ Not tested |

## Troubleshooting

### Authentication Issues
```bash
# Test connectivity
curl -s -k https://ntopng/lua/index.lua

# Check credentials
echo "NTOP_URL: $NTOP_URL"
echo "NTOP_USER: $NTOP_USER"
```

### No Data Returned
- Verify ntopng is capturing traffic (check interface status)
- Ensure proper permissions on network interface
- Check disk space for flow storage

## Reference Documentation

- [API Guide](references/api-guide.md) - Complete API documentation
- [Alerts Reference](references/alerts.md) - Alert types and meanings
- [Integration Guide](references/integration.md) - SIEM and automation integration

## License

MIT - See LICENSE file for details.

## Contributing

Issues and pull requests welcome at the GitHub repository.

---

**Disclaimer**: This is an unofficial skill. Not affiliated with the ntopng project or ntop.org.
