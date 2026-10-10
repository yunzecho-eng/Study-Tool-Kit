# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Required Notice: Copyright (c) 2026 Hyeonoh Hur (https://github.com/H-Hur/study-kit)
"""Regression coverage for the two installable editions and relocated Codex skills."""
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_codex', ROOT / 'scripts/build_codex.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
ROLES = {'source-scout', 'drill-designer', 'textbook-auditor', 'comprehension-auditor'}
LEARNING = {'learner-intake', 'source-index', 'curriculum-design',
            'textbook-authoring', 'textbook-revision', 'textbook-publish', 'exam-study'}
ENTRY_POINTS = {'study-start', 'study-session', 'study-review', 'study-publish'}


class CodexPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = build.render()

    def skill(self, name):
        return self.files[Path('skills') / name / 'SKILL.md'].decode()

    def install(self, directory):
        installed = directory / 'cache' / 'new-version' / 'study-kit-codex'
        for relative, content in self.files.items():
            path = installed / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        return installed

    def copy_build_inputs(self, directory):
        root = directory / 'kit'
        for folder in ['.claude-plugin', '.agents', 'codex', 'plugins']:
            shutil.copytree(ROOT / folder, root / folder)
        return root, mock.patch.multiple(
            build, ROOT=root, SOURCE=root / 'plugins/study-kit',
            OUTPUT=root / 'plugins/study-kit-codex')

    def test_source_eligibility_preserves_the_valid_package(self):
        with tempfile.TemporaryDirectory(prefix='study kit safe build ') as tmp:
            root, settings = self.copy_build_inputs(Path(tmp))
            with settings:
                self.assertEqual(self.files, build.render())
                self.assertFalse((root / 'dist').exists())

    def test_hidden_local_and_unsupported_sources_stop_before_any_write(self):
        with tempfile.TemporaryDirectory(prefix='study kit private file ') as tmp:
            root, settings = self.copy_build_inputs(Path(tmp))
            with settings:
                before = {p.relative_to(build.OUTPUT): p.read_bytes()
                          for p in build.OUTPUT.rglob('*') if p.is_file()}
                for name in ['skills/exam-study/references/.env',
                             'docs/.local/private.md', 'docs/settings.local.json',
                             'templates/credentials.txt', 'docs/unsupported.bin']:
                    private = build.SOURCE / name
                    private.parent.mkdir(parents=True, exist_ok=True)
                    private.write_text('SYNTHETIC_DO_NOT_PACKAGE\n', encoding='utf-8')
                    with self.subTest(name=name), self.assertRaisesRegex(
                            ValueError, '(Hidden|Unsupported)/local source'):
                        build.main(['--archive'])
                    self.assertFalse((root / 'dist').exists())
                    self.assertEqual(before, {p.relative_to(build.OUTPUT): p.read_bytes()
                                             for p in build.OUTPUT.rglob('*') if p.is_file()})
                    private.unlink()
                    if private.parent.name == '.local':
                        private.parent.rmdir()

    def test_unsafe_release_version_cannot_create_an_archive(self):
        with tempfile.TemporaryDirectory(prefix='study kit archive version ') as tmp:
            root, settings = self.copy_build_inputs(Path(tmp))
            with settings:
                manifest_path = build.SOURCE / '.claude-plugin/plugin.json'
                manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
                for version in ['../../outside', '..\\outside', '1.2.3/escape',
                                '1.2.3:stream', '1.2.3\n']:
                    manifest['version'] = version
                    manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
                    with self.subTest(version=version), self.assertRaisesRegex(
                            ValueError, 'Invalid release version'):
                        build.main(['--archive'])
                    self.assertFalse((root / 'dist').exists())

    def test_source_link_cannot_include_an_external_file(self):
        with tempfile.TemporaryDirectory(prefix='study kit source link ') as tmp:
            directory = Path(tmp)
            root, settings = self.copy_build_inputs(directory)
            external = directory / 'external-private.txt'
            external.write_text('SYNTHETIC_EXTERNAL_SOURCE\n', encoding='utf-8')
            with settings:
                link = build.SOURCE / 'docs/linked.txt'
                try:
                    link.symlink_to(external)
                except (OSError, NotImplementedError):
                    self.skipTest('File symlinks are unavailable without extra privileges')
                with self.assertRaisesRegex(ValueError, 'Linked package path'):
                    build.main(['--archive'])
                self.assertFalse((root / 'dist').exists())
                self.assertEqual('SYNTHETIC_EXTERNAL_SOURCE\n', external.read_text(encoding='utf-8'))

    def test_output_link_cannot_overwrite_an_external_file(self):
        with tempfile.TemporaryDirectory(prefix='study kit output link ') as tmp:
            directory = Path(tmp)
            root, settings = self.copy_build_inputs(directory)
            external = directory / 'external-important.txt'
            external.write_text('SYNTHETIC_KEEP_UNCHANGED\n', encoding='utf-8')
            with settings:
                link = build.OUTPUT / 'docs/budget.md'
                link.unlink()
                try:
                    link.symlink_to(external)
                except (OSError, NotImplementedError):
                    self.skipTest('File symlinks are unavailable without extra privileges')
                with self.assertRaisesRegex(ValueError, 'Linked package path'):
                    build.main([])
                self.assertEqual('SYNTHETIC_KEEP_UNCHANGED\n', external.read_text(encoding='utf-8'))

    def test_both_packages_retain_their_components_and_share_version(self):
        source_files = {p: hashlib.sha256(p.read_bytes()).digest()
                        for p in build.SOURCE.rglob('*') if p.is_file()}
        build.render()
        self.assertEqual(source_files, {p: hashlib.sha256(p.read_bytes()).digest()
                                        for p in source_files})
        self.assertEqual(ROLES, {p.stem for p in (build.SOURCE / 'agents').glob('*.md')})
        self.assertEqual(ENTRY_POINTS, {p.stem for p in (build.SOURCE / 'commands').glob('*.md')})
        self.assertEqual(LEARNING, {p.parent.name for p in (build.SOURCE / 'skills').glob('*/SKILL.md')})
        for name in ROLES:
            self.assertIn('\ntools:', (build.SOURCE / 'agents' / (name + '.md')).read_text(encoding='utf-8'))
        self.assertIn('~/.claude/projects/', (build.SOURCE / 'agents/comprehension-auditor.md').read_text(encoding='utf-8'))
        source_manifest = json.loads((build.SOURCE / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        codex_manifest = json.loads(self.files[Path('.codex-plugin/plugin.json')])
        self.assertEqual(source_manifest['version'], codex_manifest['version'])
        self.assertEqual('./skills/', codex_manifest['skills'])
        self.assertEqual(ENTRY_POINTS | LEARNING | ROLES,
                         {p.parent.name for p in self.files if p.name == 'SKILL.md'})

    def test_installed_editions_ship_scope_and_complete_license_texts(self):
        for relative in ['LICENSE', 'licenses/PolyForm-Noncommercial-1.0.0.txt',
                         'licenses/CC-BY-NC-SA-4.0.txt']:
            path = Path(relative)
            self.assertEqual((build.SOURCE / path).read_bytes(), self.files[path])
            incomplete = dict(self.files)
            del incomplete[path]
            with self.assertRaisesRegex(ValueError, 'Missing bundled license'):
                build.validate(incomplete)
        manifest = json.loads(self.files[Path('.codex-plugin/plugin.json')])
        self.assertEqual('PolyForm-Noncommercial-1.0.0 AND CC-BY-NC-SA-4.0', manifest['license'])

    def test_relocated_install_resolves_every_bundled_link(self):
        with tempfile.TemporaryDirectory(prefix='study kit relocated ') as tmp:
            installed = self.install(Path(tmp).resolve())
            for relative in self.files:
                if relative.suffix != '.md' or 'templates' in relative.parts:
                    continue
                p = installed / relative
                for match in build.LINK.finditer(p.read_text(encoding='utf-8')):
                    target = match[2].split('#')[0]
                    if not target or ':' in target or target.startswith('/'):
                        continue
                    resolved = (p.parent / target).resolve()
                    self.assertTrue(resolved.is_relative_to(installed), (relative, target))
                    self.assertTrue(resolved.is_file(), (relative, target))
            for name in ENTRY_POINTS | LEARNING | ROLES:
                self.assertIn('(../../docs/codex-runtime.md)', self.skill(name))
            self.assertFalse((installed / 'docs/runtime.md').exists())

    def test_exam_preset_and_plan_work_after_install_and_project_relocation(self):
        with tempfile.TemporaryDirectory(prefix='study kit exam relocated ') as tmp:
            directory = Path(tmp).resolve()
            installed = self.install(directory)
            skill = installed / 'skills/exam-study/SKILL.md'
            links = {match[2].split('#')[0] for match in build.LINK.finditer(skill.read_text(encoding='utf-8'))}
            for resource in ['references/personal-exam.md', 'templates/exam-plan.md']:
                self.assertIn(resource, links)
                resolved = (skill.parent / resource).resolve()
                self.assertTrue(resolved.is_relative_to(installed))
                self.assertTrue(resolved.is_file())
                self.assertTrue(resolved.read_text(encoding='utf-8').strip())

            # The shipped plan is copied into a separate study project. Its learner
            # links must still resolve there, rather than back into the plugin cache.
            project = directory / 'separate study project'
            docs = project / 'docs'
            docs.mkdir(parents=True)
            profile = docs / 'learner-profile.md'
            references = project / 'REFERENCES.md'
            profile.write_text('# Fixture learner profile\n', encoding='utf-8')
            references.write_text('# Fixture source index\n', encoding='utf-8')
            plan = docs / 'exam-plan.md'
            plan.write_bytes((skill.parent / 'templates/exam-plan.md').read_bytes())
            targets = set()
            for match in build.LINK.finditer(plan.read_text(encoding='utf-8')):
                target = match[2].split('#')[0]
                if not target or ':' in target or target.startswith('/'):
                    continue
                resolved = (plan.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(project), target)
                self.assertTrue(resolved.is_file(), target)
                targets.add(resolved)
            self.assertTrue({profile, references}.issubset(targets))

    def test_copied_project_instructions_resolve_only_learner_artifacts(self):
        with tempfile.TemporaryDirectory(prefix='study kit project relocated ') as tmp:
            directory = Path(tmp).resolve()
            installed = self.install(directory)
            project = directory / 'separate learner project'
            expected = {project / relative for relative in [
                'docs/learner-profile.md', 'docs/curriculum.md', 'docs/worklog.md',
                'docs/textbook-revisions.md', 'docs/toolbox-log.md', 'REFERENCES.md',
            ]}
            for artifact in expected:
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_text('# Fixture learner artifact\n', encoding='utf-8')
            instructions = project / 'AGENTS.md'
            instructions.write_bytes((installed / 'templates/PROJECT-AGENTS.md').read_bytes())
            targets = set()
            for match in build.LINK.finditer(instructions.read_text(encoding='utf-8')):
                target = match[2].split('#')[0]
                if not target or ':' in target or target.startswith('/'):
                    continue
                resolved = (instructions.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(project), target)
                self.assertTrue(resolved.is_file(), target)
                targets.add(resolved)
            self.assertEqual(expected, targets)

    def test_workflows_link_to_the_procedures_they_need(self):
        workflows = {
            'study-start': {'learner-intake', 'source-index', 'source-scout', 'curriculum-design', 'exam-study'},
            'study-session': {'comprehension-auditor', 'drill-designer', 'exam-study'},
            'study-review': {'comprehension-auditor', 'exam-study'},
            'study-publish': {'textbook-authoring', 'textbook-auditor', 'textbook-publish', 'exam-study'},
            'textbook-authoring': {'drill-designer', 'textbook-auditor'},
            'textbook-revision': {'comprehension-auditor', 'textbook-publish'},
        }
        for entry, dependencies in workflows.items():
            for dependency in dependencies:
                self.assertIn(f'(../{dependency}/SKILL.md)', self.skill(entry), (entry, dependency))
        start = self.skill('study-start')
        for name in ['PROJECT-AGENTS.md', 'worklog.md', 'toolbox-log.md', 'inbox-README.md']:
            self.assertIn(f'(../../templates/{name})', start)
        self.assertIn('docs/study-kit-style-rules.md', start)

    def test_role_contracts_cover_dispatch_evidence_and_write_ownership(self):
        runtime = self.files[Path('docs/codex-runtime.md')].decode()
        for name in ROLES:
            role = self.skill(name)
            self.assertIn('## Codex role execution', role)
            self.assertIn('do not delegate this same role again', role)
            self.assertIn(f'(../skills/{name}/SKILL.md)', runtime)
        self.assertIn('main session conducts intake', self.skill('learner-intake'))
        self.assertIn('evidence is incomplete', self.skill('comprehension-auditor'))
        self.assertNotIn('~/.claude/', self.skill('comprehension-auditor'))
        self.assertIn('does not edit the textbook or other existing files', self.skill('textbook-auditor'))

    def test_host_model_guides_and_historical_limits_are_distinct(self):
        claude = (build.SOURCE / 'docs/runtime.md').read_text(encoding='utf-8')
        codex = self.files[Path('docs/codex-runtime.md')].decode()
        self.assertIn('Opus at high reasoning', claude)
        for setting in ['gpt-6-astra', 'gpt-5.6-sol', '`high`', '`xhigh`']:
            self.assertIn(setting, codex)
        self.assertIn("inherit the parent's selected model", codex)
        self.assertIn('Respect a model choice', codex)
        budget = self.files[Path('docs/budget.md')].decode()
        current = budget.split('## Rules for current work')[1].split('## Historical operating rules')[0]
        self.assertIn('An unknown token budget alone is not a reason to stop', current)
        self.assertNotIn('150k', current)
        history = budget.split('## Historical operating rules')[1].split('## The one-line check')[0]
        for rule in ['> **① Keep the artifact written in one response under 8k tokens.',
                     '> **② Do not start unless the remaining budget is at least three times',
                     '>   **150k or more** left.']:
            self.assertIn(rule, history)
        self.assertIn('original Claude Code course', self.skill('source-index'))

    def test_conversion_does_not_rewrite_existing_links_or_code_samples(self):
        target = Path('skills/study-session/SKILL.md')
        value = ('---\nname: example\ndescription: Use `source-scout`\n---\n'
                 '`source-scout` and [`drill-designer`](../drill-designer/SKILL.md)\n'
                 '```text\n`source-scout`\n```\n')
        converted = build.link_skill_mentions(value, target)
        self.assertIn('description: Use `source-scout`', converted)
        self.assertIn('[`source-scout`](../source-scout/SKILL.md)', converted)
        self.assertIn('[`drill-designer`](../drill-designer/SKILL.md)', converted)
        self.assertIn('```text\n`source-scout`\n```', converted)

    def test_validator_rejects_broken_host_links_and_foreign_instructions(self):
        path = Path('skills/source-scout/SKILL.md')
        original = self.files[path]
        variants = [
            original.replace(b'../../docs/codex-runtime.md', b'../../docs/missing.md'),
            original.replace(b'## Codex role execution', b'## Unspecified role'),
            original + b'\nRead ~/.claude/projects/current/*.jsonl\n',
            original + b'\nRun /study-kit:study-start\n',
            original.replace(b'name: source-scout', b'name: source-scout\nmodel: opus'),
        ]
        for value in variants:
            files = dict(self.files)
            files[path] = value
            with self.subTest(value=value[-80:]), self.assertRaises(ValueError):
                build.validate(files)

    def test_validator_rejects_missing_or_replaced_exam_skill(self):
        path = Path('skills/exam-study/SKILL.md')
        for replacement in [None, Path('skills/unexpected-mode/SKILL.md')]:
            files = dict(self.files)
            content = files.pop(path)
            if replacement is not None:
                files[replacement] = content.replace(b'name: exam-study', b'name: unexpected-mode')
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ValueError, 'Unexpected skill set'):
                build.validate(files)


if __name__ == '__main__':
    unittest.main()
