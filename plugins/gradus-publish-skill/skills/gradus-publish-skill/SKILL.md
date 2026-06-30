---
name: gradus-publish-skill
description: Use ao querer PUBLICAR ou ATUALIZAR uma skill no repo de marketplace do time (gradus-skills-MU no GitHub), deixando-a instalável via /plugin pelos colegas. Gatilhos — "subir essa skill", "publicar a skill no github", "atualizar a skill no marketplace", "deixar a skill disponível pro time", "commitar a skill". NÃO use para commitar código dos sistemas Gradus Tech (isso é gradus-github-commit) nem para criar uma skill nova do zero (writing-skills).
---

# Publicar skill no marketplace Gradus

Embrulha uma skill como **plugin à la carte** (1 plugin por skill) no repo `gradus-skills-MU`, registra no
`marketplace.json`, valida, commita+push, e re-aponta o junction de dev. O trabalho mecânico está no script —
esta skill é o gatilho + o julgamento.

## Quando usar · quando NÃO
- **Usar:** uma skill (em `~/.claude/skills/<nome>`) está pronta e você quer disponibilizá-la pro time / atualizá-la no repo.
- **NÃO usar:** commit nos sistemas Gradus Tech → `gradus-github-commit`. Criar/editar a skill em si → `superpowers:writing-skills`.

## Como rodar
Da raiz do repo (ou qualquer lugar):
```
python -X utf8 scripts/publish_skill.py <nome-skill> [--source DIR] [--repo DIR] [--no-push] [--dry-run]
```
- `<nome-skill>`: o nome da pasta da skill. Default `--source` = `~/.claude/skills/<nome>`; `--repo` = `~/gradus-skills`.
- **Sempre rode `--dry-run` primeiro** para conferir o plano (NOVA vs ATUALIZAR, destino, descrição).
- O script: copia (se NOVA) → `plugin.json` → registra no `marketplace.json` → `claude plugin validate` (trava: só
  segue se passar) → `git add/commit/push` → re-aponta o junction `~/.claude/skills/<nome>` p/ o repo.

## Julgamento (o que o script NÃO decide por você)
- A **descrição** do plugin vem do frontmatter `description` da SKILL.md — garanta que ela esteja boa (é o que
  faz a skill ser descoberta). Se estiver fraca, ajuste a SKILL.md ANTES de publicar.
- **Skill genérica?** O repo é compartilhado — evite travar referências específicas de um projeto na skill
  (use placeholders + exemplos marcados). Veja o padrão das skills existentes.
- `--no-push` se quiser revisar o commit local antes de subir. Push exige `gh auth`/credencial git já configurada.

## Depois
A skill fica instalável: `/plugin marketplace add gradusmsimao/gradus-skills-MU` + `/plugin install <nome>@<marketplace>`.
Quem edita a skill (autor) continua pelo junction de dev; re-publicar uma já-publicada = só rodar de novo (caso ATUALIZAR).
