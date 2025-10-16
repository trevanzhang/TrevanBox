# TrevanBox - Personal Cognitive Enhancement Operating System

English | [中文版](README_CN.md)

> **A personal knowledge management system based on PARA methodology, transforming information into actionable insights and records into catalysts for growth.**

## 🎯 Project Overview

TrevanBox is a personal cognitive enhancement operating system built upon the PARA (Projects, Areas, Resources, Archives) methodology. It transcends conventional note-taking applications to provide a comprehensive personal knowledge management solution that empowers users to convert scattered information into organized knowledge and transform daily documentation into momentum for personal development.

### Core Philosophy
- **Action-Oriented**: All organizational structures serve to facilitate more effective action
- **Growth-Driven**: Every element is designed to contribute to personal development
- **Long-Term Vision**: Establish a system capable of sustainable evolution
- **Minimalist Principles**: Maximum impact through essential guidelines

## 🏗️ System Architecture

```
TrevanBox/
├── 0-Inbox/pending/          # Cognitive Gateway: Temporary storage and processing of new information
├── 1-Projects/               # Action Focus: Concrete implementation of short-term objectives
├── 2-Areas/                  # Life Pillars: Continuous maintenance of long-term responsibilities
│   ├── Personal-Growth/      # Personal Development (includes journal entries)
│   ├── Health/               # Health Management
│   ├── Finance/              # Financial Planning
│   ├── Career/               # Professional Development
│   └── Family/               # Family Life
├── 3-Resources/              # Knowledge Repository: Content with potential future utility
├── 4-Archives/               # Experience Accumulation: Inactive yet valuable content
├── Assets/                   # Attachment Directory: Configure for Obsidian attachments
├── docs/                     # System Documentation: Usage guides and protocol documentation
├── scripts/                  # Automation Tools: Cognitive load reduction utilities
├── templates/                # Thinking Frameworks: Standardized content templates
├── follow/                   # RSS Import: Automated information stream collection
├── clippings/                # Web Excerpts: Rapid capture of inspiration
├── readwise/                 # Reading Notes: Systematic knowledge collection
├── zotero/                   # Academic Resources: Research content organization
├── webdav/                   # Cross-Platform Synchronization: Multi-device recording and cloud storage
├── manual/                   # Manual Import: Copy-paste and custom content
└── ainotes/                  # AI Content: Storage for AI-generated responses and creative ideas
```

## 🚀 Quick Start

### 1. System Requirements
- **Obsidian**: Recommended v1.7+ or later
- **Python 3.8+**: Required for AI preprocessor and automation scripts
- **uv**: Modern Python package manager (highly recommended)
- **Ollama**: Local AI model execution (optional, for intelligent processing)
- **Operating System**: Compatible with Windows, macOS, Linux
- **Optional Plugins**: Templater, Dataview, QuickAdd

### 2. Installation

#### Method 1: Using uv (Recommended)
```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/macOS
# Or visit https://docs.astral.sh/uv/getting-started/installation/ for Windows installation

# 2. Clone the repository
git clone https://github.com/your-username/TrevanBox.git
cd TrevanBox

# 3. Launch AI preprocessor (automatically creates virtual environment and installs dependencies)
./scripts/preprocessor.sh --help
```

#### Method 2: Traditional Python Environment
```bash
# 1. Clone the repository
git clone https://github.com/your-username/TrevanBox.git
cd TrevanBox

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### 3. Basic Configuration
1. **Obsidian Setup**: Open project root directory, configure core plugins
2. **AI Model Configuration**: Launch Ollama, download required models (e.g., qwen2.5:7b)
3. **Metadata Standards**: Adopt YAML frontmatter format
4. **Tag System**: Utilize structured tags for content classification
5. **File Naming**: English directory names, journal files in YYYY-MM-DD.md format

## 📋 Core Features

### PARA Classification System
- **Projects**: Short-term endeavors with clear completion objectives
- **Areas**: Long-term responsibilities requiring continuous maintenance
- **Resources**: Topics or interests with potential future utility
- **Archives**: Inactive content from the previous three categories

### Import Sources
- **follow**: Automated RSS subscription content collection
- **clippings**: Obsidian browser plugin excerpts
- **readwise**: Systematic reading notes collection
- **zotero**: Academic literature and reference materials
- **webdav**: Cross-platform cloud storage synchronization
- **manual**: Manual import and copy-paste content
- **ainotes**: AI-generated content preservation

### AI-Powered Intelligent Tools
- **preprocessor.sh**: uv-based AI preprocessor for intelligent content analysis and metadata generation
- **ollama/prehandler.py**: Core AI preprocessing engine supporting automatic classification and tag recommendations
- **Professional AI Assistant Agent System**: 18 specialized agents covering core domains including data analysis, research analysis, and productivity enhancement

### Automation Tools
- **cleanup.sh**: Clean import directories, move to pending processing
- **move-to-inbox.sh**: File relocation operations
- **Claude Command System**: Complete PARA workflow command suite (see docs/claude-commands.md)

### Template System
- **Project Note Template**: Objectives + Deadlines + Action Items
- **Area Maintenance Template**: Standards + Review Frequency
- **Resource Collection Template**: Utility + Difficulty Assessment
- **Journal Template**: Growth Records + Reflections + Connections
- **Imported Content Template**: Standardization + Classification Suggestions

## 🔄 Workflow

### Daily Operations
1. **Intelligent Content Processing**: Import → `/para-process` AI Analysis → `/para-organize` Intelligent Classification → PARA Distribution
2. **Project Advancement**: `/para-project` Create and manage projects → Consolidate relevant resources → Focus on execution → Complete and archive
3. **Area Maintenance**: `/para-area` Check area health → Assess maintenance quality → Incubate new projects → Continuous improvement
4. **Resource Collection**: Collect by interest in 3-Resources → Periodically evaluate utility → Archive as needed
5. **Journal Writing**: Daily documentation → Identify action items → Link to relevant PARA content
6. **System Review**: `/para-review` Standardized review → Summarize experiences → Adjust plans → Continuous optimization

### Maintenance Rhythm
- **Weekly 5-Minute Review**: Rename, categorize, update project status
- **Monthly Review**: Evaluate area maintenance quality, clean outdated resources
- **Quarterly Deep Review**: Identify reusable materials from archives, adjust PARA structure

## 📚 Documentation Structure

| Document | Description |
|----------|-------------|
| [CLAUDE.md](./CLAUDE.md) | System Manifesto and Architecture Guide |
| [CHANGELOG.md](./CHANGELOG.md) | Version Update Records and Cognitive Evolution |
| [docs/para-rules.md](./docs/para-rules.md) | Detailed PARA Classification Rules |
| [docs/tag-system.md](./docs/tag-system.md) | Tag System Usage Guide |
| [docs/journal-guide.md](./docs/journal-guide.md) | Journal Integration with PARA Practice Guide |
| [docs/claude-commands.md](./docs/claude-commands.md) | Complete Claude Command System Guide |
| [docs/agents.md](./docs/agents.md) | Professional AI Assistant Agent System Guide |
| [docs/ai-preprocessor.md](./docs/ai-preprocessor.md) | AI Preprocessor Usage Instructions |

## 🛠️ Technical Specifications

### Metadata Standards
```yaml
---
created: 2025-10-15T10:30:00+08:00    # Creation time (ISO format)
updated: 2025-10-15T18:45:00+08:00    # Update time
status: sprout|evergreen|discharged    # Content lifecycle status
type: project|area|resource|journal    # Content type classification
tags: [tag1, tag2]                     # Structured tags
area: "Personal-Growth"                #所属领域 (optional)
---
```

### Tag Classification
- **Source Tags**: #follow, #clippings, #readwise, #zotero, #webdav, #manual, #ainotes
- **Status Tags**: #pending, #processed, #needs-organization, #to-archive
- **PARA Classification Tags**: #project/active, #area/health, #resource/learning, etc.
- **Content Type Tags**: #excerpt, #idea, #task, #meeting, #learning, etc.
- **Priority Tags**: #high-priority, #medium-priority, #low-priority

## 🎯 Use Cases

### Individual Users
- **Knowledge Management**: Systematic collection, organization, and retrieval of personal knowledge
- **Project Management**: Planning and execution tracking of short-term objectives
- **Growth Documentation**: Visualization of personal development and learning trajectories
- **Creative Management**: Inspiration collection and idea incubation

### Professionals
- **Researchers**: Literature management and knowledge system construction
- **Content Creators**: Material collection and creative workflow management
- **Product Managers**: Requirement organization and project advancement
- **Freelancers**: Multi-project management and knowledge reuse

## 🔮 Future Development

### Current Phase (v1.2.1) - Professional AI Assistant Integration ✅
- Complete PARA system architecture
- Standardized metadata system
- Fundamental automation scripts
- Journal integration into growth domain
- Documentation and template system
- **AI Preprocessor Integration**: Ollama-based intelligent content analysis
- **Claude Command System**: Complete PARA workflow command suite
- **Automated Metadata Generation**: Automatic extraction of titles, tags, and summaries
- **Intelligent Classification Suggestions**: AI-assisted PARA classification recommendations
- **uv Environment Management**: Unified Python environment and dependency management
- **Intelligent Dependency Handling**: Automatic checking and installation of missing dependencies
- **Cross-Platform Compatibility**: Unified experience across Windows/Linux/macOS
- **Professional AI Assistant Agent System**: 18 specialized agents covering core domains
- **Agent Collaboration Workflows**: Three collaboration modes for data analysis, research analysis, and productivity enhancement
- **Intelligent Tool Integration**: Each agent equipped with professional toolsets supporting complex task processing
- **Multi-Language Support**: Chinese and English agents for diverse usage scenarios

### Next Phase (v2.0) - Deep Intelligence
- Automatic relationship discovery and knowledge graph construction
- Personalized usage pattern learning and optimization
- Cross-domain content association and recommendations
- Intelligent goal planning and progress tracking

### Future Phase (v3.0) - Cognitive Assistant
- Personal cognitive pattern analysis and personalized recommendations
- Historical data-based intelligent goal planning
- Knowledge gap identification and learning path recommendations
- Creative stimulation and thinking tool integration

## 🤝 Contributing Guidelines

### Issue Reporting
- Use Issues to report bugs and feature requests
- Provide detailed problem descriptions and reproduction steps
- Include system environment and usage scenario information

### Feature Suggestions
- Propose feature improvement suggestions in Issues
- Describe use cases and expected outcomes
- Provide specific implementation approaches

### Documentation Enhancement
- Help improve usage documentation and best practices
- Share personal usage experiences and techniques
- Translate documentation to other languages

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- **PARA Methodology**: Thanks to Tiago Forte for proposing the PARA knowledge management method
- **Obsidian Community**: Thanks to the extensive user base for sharing best practices and experiences
- **Open Source Projects**: Thanks to all open-source tools that provided inspiration for this project

## 🛠️ Development Environment

### Python Environment Management (uv-based)
- **Unified Environment Management**: Use uv tool to manage all Python dependencies and virtual environments
- **Automatic Dependency Installation**: Scripts automatically check and install missing dependency packages at startup
- **Intelligent Cache Optimization**: Leverage uv's efficient caching and parallel processing capabilities
- **Cross-Platform Compatibility**: Unified user experience across Windows/Linux/macOS
- **Environment Isolation**: `.venv` directory ensures project environment independence, avoiding dependency conflicts

### AI Model Integration
- **Ollama Integration**: Support local AI model execution, protecting data privacy
- **Intelligent Content Processing**: Automatic analysis, classification, and metadata generation
- **Multi-Model Support**: Support for qwen2.5, llama3, and various other models
- **Custom Prompts**: Configurable AI processing templates

---

**Project Version**: v1.2.1
**Creation Date**: 2025-10-15
**Last Updated**: 2025-10-17
**Maintainers**: TrevanBox Team
**Core Philosophy**: Transforming information into actionable insights and records into catalysts for growth
**Technical Features**: AI intelligent processing, Claude command integration, PARA methodology implementation, uv environment management, professional AI assistant agent system

*This is not merely a tool, but a systematic implementation of a cognitive methodology.*