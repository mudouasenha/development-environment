# Windows VS Code Extension Evaluation

Date: 2026-04-12
Source scanned: `/mnt/c/Users/mathe/.vscode/extensions`

## Executive Summary

Your Windows VS Code environment is broad and capable, but it is not curated.

- `111` extension directories were present.
- Those resolve to `101` unique extensions.
- `10` directories are stale duplicate-version installs.
- The strongest part of the setup is polyglot tooling: .NET, Python, Rust, Go, Docker, WSL, Terraform, GraphQL, Markdown, and general web development are all represented.
- The weakest part is overlap: too many AI assistants, snippet packs, legacy test adapters, and old extension-pack residue.

The recommendation is to move to a smaller baseline and keep specialist tools in profiles or disabled-by-default.

## Recommended Curated Baseline

This is the set I would keep enabled as your default Windows profile.

- `Anthropic.claude-code`
- `openai.chatgpt`
- `eamodio.gitlens`
- `GitHub.vscode-pull-request-github`
- `esbenp.prettier-vscode`
- `dbaeumer.vscode-eslint`
- `bradlc.vscode-tailwindcss`
- `DavidAnson.vscode-markdownlint`
- `redhat.vscode-yaml`
- `humao.rest-client`
- `docker.docker`
- `ms-vscode-remote.remote-wsl`
- `ms-vscode-remote.remote-containers`
- `ms-dotnettools.csharp`
- `ms-dotnettools.csdevkit`
- `josefpihrt-vscode.roslynator`
- `ms-vscode.powershell`
- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-python.vscode-python-envs`
- `rust-lang.rust-analyzer`
- `golang.go`
- `hashicorp.terraform`
- `GraphQL.vscode-graphql`
- `PKief.material-icon-theme`

Notes:

- Keep one AI pair, not five AI agents. My recommendation is `Anthropic.claude-code` as the primary coding agent and `openai.chatgpt` as the secondary.
- Keep one icon theme and one color theme. `PKief.material-icon-theme` is the best universal icon choice from your current set.

## Keep Only If You Actively Use The Stack

These are good extensions, but they should be profile-specific or disabled unless you use them weekly.

### .NET and Microsoft stack

- `Ionide.Ionide-fsharp`
- `ms-dotnettools.dotnet-interactive-vscode`
- `ms-dotnettools.vscode-dotnet-pack`
- `ms-dotnettools.vscode-dotnet-runtime`
- `ms-mssql.mssql`
- `ms-mssql.data-workspace-vscode`
- `ms-mssql.sql-bindings-vscode`
- `ms-mssql.sql-database-projects-vscode`
- `adpyke.vscode-sql-formatter`

### Python and notebooks

- `ms-python.debugpy`
- `ms-toolsai.jupyter`
- `ms-toolsai.jupyter-keymap`
- `ms-toolsai.jupyter-renderers`
- `ms-toolsai.vscode-jupyter-cell-tags`
- `ms-toolsai.vscode-jupyter-slideshow`
- `batisteo.vscode-django`
- `wholroyd.jinja`
- `KevinRose.vsc-python-indent`
- `njpwerner.autodocstring`

### Cloud, containers, infrastructure

- `ms-kubernetes-tools.vscode-kubernetes-tools`
- `ms-azuretools.vscode-azureresourcegroups`
- `ms-azuretools.vscode-azure-mcp-server`
- `ms-azuretools.vscode-azure-github-copilot`
- `ms-azuretools.vscode-containers`
- `ms-azuretools.vscode-docker`

### Language-specific or niche

- `ms-vscode.cpptools`
- `redhat.java`
- `GraphQL.vscode-graphql-syntax`
- `stripe.vscode-stripe`
- `GrapeCity.gc-excelviewer`
- `pomdtr.excalidraw-editor`
- `firefox-devtools.vscode-firefox-debug`
- `ms-edgedevtools.vscode-edge-devtools`
- `GitHub.codespaces`
- `GitHub.remotehub`
- `ms-vscode.remote-repositories`
- `paulys.fluent-syntax-highlighting`
- `adpyke.codesnap`
- `shd101wyy.markdown-preview-enhanced`
- `yzhang.markdown-all-in-one`
- `rangav.vscode-thunder-client`

## High-Confidence Remove Or Disable Candidates

These are the extensions I would cut first.

### Clear redundancy or legacy residue

- `BracketPairColorDLW.bracket-pair-color-dlw`
Reason: bracket coloring is built into modern VS Code.

- `dustypomerleau.rust-syntax`
Reason: `rust-lang.rust-analyzer` already covers Rust far better.

- `donjayamanne.python-environment-manager`
Reason: deprecated and superseded by `ms-python.vscode-python-envs`.

- `donjayamanne.python-extension-pack`
Reason: extension packs are unnecessary once you already manage the individual tools.

- `littlefoxteam.vscode-python-test-adapter`
Reason: legacy test adapter pattern; the Python extension and native VS Code testing are better.

- `hbenl.vscode-test-explorer`
Reason: old adapter UI ecosystem; VS Code testing is now native.

- `ms-vscode.test-adapter-converter`
Reason: only useful for the old adapter path you should be exiting.

- `premparihar.gotestexplorer`
Reason: `golang.go` already covers Go testing well enough.

- `formulahendry.code-runner`
Reason: convenient, but noisy and usually a downgrade from proper task or terminal workflows.

- `ritwickdey.LiveServer`
Reason: useful for simple static pages, but redundant if you already use framework dev servers.

- `VisualStudioExptTeam.vscodeintellicode`
Reason: low-value next to modern AI tooling and language servers.

- `VisualStudioExptTeam.intellicode-api-usage-examples`
Reason: support extension for IntelliCode; remove with it.

### AI overlap

- `GitHub.copilot-chat`
- `kilocode.kilo-code`
- `ms-windows-ai-studio.windows-ai-studio`
- `ms-azuretools.vscode-azure-github-copilot`

Reason: too many competing chat/agent surfaces. Pick one primary, one secondary, and disable the rest.

### Snippet overload

- `burkeholland.simple-react-snippets`
- `dsznajder.es7-react-js-snippets`
- `infeng.vscode-react-typescript`
- `rodrigovallades.es7-react-js-snippets`
- `jorgeserrano.vscode-csharp-snippets`

Reason: these overlap heavily and increase suggestion noise. Keep at most one React snippet pack and only keep C# snippets if you still miss native completions.

### Old convenience extensions that built-ins have mostly replaced

- `formulahendry.auto-rename-tag`
- `christian-kohler.npm-intellisense`
- `christian-kohler.path-intellisense`
- `pmneo.tsimporter`
- `ChristianAlexander.flip`
- `kenhowardpdx.vscode-gist`
- `naumovs.color-highlight`

Reason: useful once, but low leverage compared with current editor features and language servers.

## Theme Recommendation

Choose one color theme and disable the rest.

- Keep: `akamud.vscode-theme-onedark`
- Review: `azemoh.one-monokai`
- Review: `rokoroku.vscode-theme-darcula`

## C# Recommendation

Your strongest C# set is:

- `ms-dotnettools.csharp`
- `ms-dotnettools.csdevkit`
- `josefpihrt-vscode.roslynator`
- `ms-vscode.powershell`

Review these separately:

- `adrianwilczynski.namespace`
- `k--kato.docomment`
- `kreativ-software.csharpextensions`

They are not bad, but they are quality-of-life extras, not core tooling.

## Python Recommendation

Your lean Python set should be:

- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-python.vscode-python-envs`
- `ms-python.debugpy`

Add these only if needed:

- `ms-toolsai.jupyter`
- `batisteo.vscode-django`
- `wholroyd.jinja`
- `njpwerner.autodocstring`

Remove:

- `donjayamanne.python-extension-pack`
- `donjayamanne.python-environment-manager`
- `littlefoxteam.vscode-python-test-adapter`

## API Client Recommendation

Keep one API client.

- Keep by default: `humao.rest-client`
- Disable unless you prefer the UI: `rangav.vscode-thunder-client`

## Duplicate-Version Cleanup

These ids had multiple versions present in the extensions directory:

- `GitHub.copilot-chat`: `0.42.3`, `0.43.0`
- `ms-dotnettools.csdevkit`: `3.10.14`, `3.11.200`
- `ms-kubernetes-tools.vscode-kubernetes-tools`: `1.3.28`, `1.3.29`
- `ms-toolsai.jupyter`: `2024.11.0`, `2025.2.0`, `2025.3.0`, `2025.5.0`, `2025.9.0`, `2025.9.1`
- `ms-vscode-remote.remote-wsl`: `0.88.5`, `0.99.0`, `0.104.3`

Important note:

- Multiple version directories do not always mean all versions are active.
- They do mean the Windows VS Code extensions folder has update residue and is worth cleaning.

## Curated List By Use Case

If you want a smaller and cleaner setup, I recommend these profiles.

### Default daily profile

- `Anthropic.claude-code`
- `openai.chatgpt`
- `eamodio.gitlens`
- `GitHub.vscode-pull-request-github`
- `esbenp.prettier-vscode`
- `dbaeumer.vscode-eslint`
- `DavidAnson.vscode-markdownlint`
- `redhat.vscode-yaml`
- `humao.rest-client`
- `docker.docker`
- `ms-vscode-remote.remote-wsl`
- `ms-vscode-remote.remote-containers`
- `PKief.material-icon-theme`
- `akamud.vscode-theme-onedark`

### Web and TypeScript profile

- `bradlc.vscode-tailwindcss`
- `GraphQL.vscode-graphql`
- `YoavBls.pretty-ts-errors`

### .NET profile

- `ms-dotnettools.csharp`
- `ms-dotnettools.csdevkit`
- `josefpihrt-vscode.roslynator`
- `ms-vscode.powershell`
- `ms-dotnettools.dotnet-interactive-vscode`

### Python profile

- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-python.vscode-python-envs`
- `ms-python.debugpy`
- `ms-toolsai.jupyter`

### Infra profile

- `hashicorp.terraform`
- `redhat.vscode-yaml`
- `ms-kubernetes-tools.vscode-kubernetes-tools`
- `docker.docker`

## Full Inventory Assessment

### Keep

- `Anthropic.claude-code`
- `DavidAnson.vscode-markdownlint`
- `GitHub.vscode-pull-request-github`
- `GraphQL.vscode-graphql`
- `PKief.material-icon-theme`
- `YoavBls.pretty-ts-errors`
- `akamud.vscode-theme-onedark`
- `bradlc.vscode-tailwindcss`
- `dbaeumer.vscode-eslint`
- `docker.docker`
- `eamodio.gitlens`
- `esbenp.prettier-vscode`
- `golang.go`
- `hashicorp.terraform`
- `humao.rest-client`
- `josefpihrt-vscode.roslynator`
- `ms-dotnettools.csharp`
- `ms-dotnettools.csdevkit`
- `ms-python.python`
- `ms-python.vscode-pylance`
- `ms-python.vscode-python-envs`
- `ms-vscode-remote.remote-containers`
- `ms-vscode-remote.remote-wsl`
- `ms-vscode.powershell`
- `openai.chatgpt`
- `redhat.vscode-yaml`
- `rust-lang.rust-analyzer`

### Keep If Active

- `GrapeCity.gc-excelviewer`
- `GraphQL.vscode-graphql-syntax`
- `GitHub.codespaces`
- `GitHub.remotehub`
- `Ionide.Ionide-fsharp`
- `KevinRose.vsc-python-indent`
- `adpyke.codesnap`
- `adpyke.vscode-sql-formatter`
- `adrianwilczynski.namespace`
- `batisteo.vscode-django`
- `firefox-devtools.vscode-firefox-debug`
- `k--kato.docomment`
- `kreativ-software.csharpextensions`
- `ms-azuretools.vscode-azure-github-copilot`
- `ms-azuretools.vscode-azure-mcp-server`
- `ms-azuretools.vscode-azureresourcegroups`
- `ms-azuretools.vscode-containers`
- `ms-azuretools.vscode-docker`
- `ms-dotnettools.dotnet-interactive-vscode`
- `ms-dotnettools.vscode-dotnet-pack`
- `ms-dotnettools.vscode-dotnet-runtime`
- `ms-edgedevtools.vscode-edge-devtools`
- `ms-kubernetes-tools.vscode-kubernetes-tools`
- `ms-mssql.data-workspace-vscode`
- `ms-mssql.mssql`
- `ms-mssql.sql-bindings-vscode`
- `ms-mssql.sql-database-projects-vscode`
- `ms-python.debugpy`
- `ms-toolsai.jupyter`
- `ms-toolsai.jupyter-keymap`
- `ms-toolsai.jupyter-renderers`
- `ms-toolsai.vscode-jupyter-cell-tags`
- `ms-toolsai.vscode-jupyter-slideshow`
- `ms-vscode.cpptools`
- `ms-vscode.remote-repositories`
- `ms-vscode.vscode-typescript-next`
- `njpwerner.autodocstring`
- `paulys.fluent-syntax-highlighting`
- `pomdtr.excalidraw-editor`
- `rangav.vscode-thunder-client`
- `redhat.java`
- `shd101wyy.markdown-preview-enhanced`
- `stripe.vscode-stripe`
- `wholroyd.jinja`
- `yzhang.markdown-all-in-one`
- `azemoh.one-monokai`
- `rokoroku.vscode-theme-darcula`

### Remove Or Disable

- `BracketPairColorDLW.bracket-pair-color-dlw`
- `ChristianAlexander.flip`
- `GitHub.copilot-chat`
- `VisualStudioExptTeam.intellicode-api-usage-examples`
- `VisualStudioExptTeam.vscodeintellicode`
- `burkeholland.simple-react-snippets`
- `christian-kohler.npm-intellisense`
- `christian-kohler.path-intellisense`
- `donjayamanne.python-environment-manager`
- `donjayamanne.python-extension-pack`
- `dsznajder.es7-react-js-snippets`
- `dustypomerleau.rust-syntax`
- `formulahendry.auto-rename-tag`
- `formulahendry.code-runner`
- `hbenl.vscode-test-explorer`
- `infeng.vscode-react-typescript`
- `jorgeserrano.vscode-csharp-snippets`
- `kenhowardpdx.vscode-gist`
- `kilocode.kilo-code`
- `littlefoxteam.vscode-python-test-adapter`
- `ms-vscode.test-adapter-converter`
- `ms-windows-ai-studio.windows-ai-studio`
- `naumovs.color-highlight`
- `pmneo.tsimporter`
- `premparihar.gotestexplorer`
- `ritwickdey.LiveServer`
- `rodrigovallades.es7-react-js-snippets`

## Bottom Line

Your current setup is that of a power user, but not yet that of a disciplined profile-based setup.

If I were simplifying it for daily use, I would:

1. Keep the curated baseline only.
2. Choose one main AI assistant and one backup.
3. Remove legacy test-adapter extensions.
4. Remove deprecated Python tooling.
5. Clean stale duplicate extension versions.
6. Move notebooks, Azure, SQL, Java, C++, and niche tools into separate VS Code profiles.
