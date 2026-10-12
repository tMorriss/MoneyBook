# Plan: Fix Quadlet service enable error in jenkins.sh

## Problem Description
When executing `jenkins.sh` in Jenkins, the build fails at step:
`Failed to enable unit: Unit /run/user/1000/systemd/generator/moneybook-pod.service is transient or generated.`

This is caused by running `systemctl --user enable` on Quadlet-generated systemd unit files, which systemd prohibits.
Quadlet handles unit enablements automatically during `systemctl --user daemon-reload` based on `[Install] WantedBy=default.target` in Quadlet definition templates.

## Proposed Changes
1. Remove `systemctl --user enable` step from `build/jenkins.sh`.
2. Add a work plan file `docs/plans/2026-10-12-fix-quadlet-jenkins-enable-plan.md`.
3. Complete pre-commit verification steps.
4. Submit changes.

## Steps
1. Create plan document under `docs/plans/2026-10-12-fix-quadlet-jenkins-enable-plan.md`.
2. Modify `build/jenkins.sh` to remove `systemctl --user enable`.
3. Complete pre commit steps to ensure proper testing, verification, review, and reflection are done.
4. Submit the changes.
