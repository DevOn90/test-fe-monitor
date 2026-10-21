## Metadata

- **Project**: <name-of-project>
- **Status**: <Draft-In-Progress-Completed-Superseded>
- **Stage**: <discovery-delivery>
- **Owner**: <name-of-owner>
- **Last Updated**: <YYYY-MM-DD>

---

## Related Documents

- PRD: <!-- link -->
- Release Plan: <!-- link -->
- Issues: <!-- e.g. #123 -->
- PRs: <!-- e.g. #125 -->

---

# Release Runbook [RRB-XXX]: <Name of Release>

## Release Summary

- **Release Version**: <!--e.g. v1.1.0-->
- **Environment**: <!--prod / staging / pi5-->
- **Target Host**: <!--server / device / cluster-->
- **Release Goal**: <!--one sentence-->
- **Deployment Window**: <!--date/time-->

---

## Included Scope

- <!--feature / issue / PR-->
- <!--feature / issue / PR-->

## Excluded Scope

- <!--explicitly not included-->

---

## Prerequisites

- [ ] All required PRs merged
- [ ] Build passes
- [ ] Environment variables / secrets configured
- [ ] Backups created if needed
- [ ] Monitoring available
- [ ] Rollback path confirmed

---

## Deployment Steps
<!--E.g.:
1. Pull latest code / checkout release tag
2. Build application or image
3. Publish artifact if needed
4. Run database migration if needed
5. Deploy to target environment
6. Restart service / container
7. Confirm service is healthy
-->

1. ...
2. ...
3. ...

---

## Verification Steps

- [ ] Application starts successfully
- [ ] Health endpoint responds
- [ ] Core user flow works
- [ ] Logs show no critical errors
- [ ] Monitoring shows normal CPU / memory / error rate

---

## Validation Window

- **Duration**: <!--e.g. 7 days-->
- **Metrics to watch**:
1. <!--uptime target-->
2. <!--error-rate target-->
3. <!--business metric target-->

---

## Rollback Criteria

Rollback if any of the following occur:

- <!--critical user flow broken-->
- <!--error rate above threshold-->
- <!--service unavailable for threshold duration-->

---

## Rollback Steps
<!-- E.g.:
1. Stop current release
2. Re-deploy previous stable version
3. Restore previous config or image tag
4. Verify service health
5. Confirm core user flow works again
-->

1. ...
2. ...
3. ...

---

## Post-Release Notes

- **Release Result**: <!--successful / rolled back / partial-->
- **Observed Issues**: <!--list any issues observed during release-->
- **Follow-up Actions**: <!--list any follow-up actions needed-->
- **Decision**: <!--close PRD / hotfix / new release-->

---

## References

- Monitoring dashboard: <!-- link -->
- Deployment script: <!-- link -->
- Rollback artifact/version: <!-- link -->
