pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '30'))
        timeout(time: 120, unit: 'MINUTES')
    }

    // triggers {
    //     cron('0 14 * * 1')
    // }

    parameters {
        string(
            name: 'DEFAULT_EMAIL',
            defaultValue: 'usman.arshad@rolustech.com',
            description: 'Primary recipient for pipeline report emails.'
        )
        string(
            name: 'ADDITIONAL_EMAILS',
            defaultValue: '',
            description: 'Additional email recipients (comma-separated list).'
        )
        string(
            name: 'DAKOTA_CREDENTIALS_ID',
            defaultValue: 'dakota-portal-creds',
            description: 'Jenkins credential ID for Dakota portal login (DAKOTA_USERNAME / DAKOTA_PASSWORD).'
        )
        string(
            name: 'INFRA_RETRY_COUNT',
            defaultValue: '3',
            description: 'Maximum retries for allowed infra failures (0 disables retries).'
        )
        booleanParam(
            name: 'RUN_SMOKE_ONLY',
            defaultValue: false,
            description: 'Run only the smoke subset (~8 critical tests) instead of the full 43-test suite.'
        )
        booleanParam(
            name: 'RUN_ALLURE',
            defaultValue: true,
            description: 'Generate and publish Allure report in Jenkins.'
        )
        booleanParam(
            name: 'SEND_EMAIL',
            defaultValue: true,
            description: 'Send HTML email summary after pipeline completion.'
        )
    }

    environment {
        VENV_DIR = '.venv-jenkins'
        DAKOTA_HEADLESS = '1'
        CHROME_WINDOW_WIDTH = '1920'
        CHROME_WINDOW_HEIGHT = '1080'
        CHROME_USER_DATA_CLEANUP = 'true'
        CHROME_USER_DATA_DIR = "${WORKSPACE}\\jenkins-chrome-profile"
        CI = 'true'
        PYTHONIOENCODING = 'UTF-8'
        PYTHONUNBUFFERED = '1'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PYTEST_JUNIT = 'test-results/pytest.xml'
        PYTEST_HTML = 'test-results/report.html'
        PYTEST_JSON = 'test-results/report.json'
        ALLURE_DIR = 'allure-results'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    if (!fileExists('requirements.txt')) {
                        error('Checkout failed — requirements.txt not found in repository.')
                    }
                    def shortCommit = env.GIT_COMMIT ? env.GIT_COMMIT.take(7) : 'N/A'
                    currentBuild.description = 'Dakota Chrome Extension | UI Functional Suite'
                    echo "Repo: https://github.com/TestWithMani/dakota_chrome_ext_ui"
                    echo "Branch: ${env.BRANCH_NAME ?: 'main'} | Commit: ${shortCommit}"
                    // def effectiveCfg = getEffectiveRunConfig()
                    // if (effectiveCfg.scheduledBuild) {
                    //     echo 'Scheduled run detected: applying Monday 2:00 PM email preset.'
                    // }
                }
            }
        }

        stage('Resolve Python') {
            steps {
                script {
                    runShell(
                        """
                            set -e
                            BASE_PY=""
                            if [ -z "\$BASE_PY" ] && command -v python3 >/dev/null 2>&1; then BASE_PY="\$(command -v python3)"; fi
                            if [ -z "\$BASE_PY" ] && command -v python >/dev/null 2>&1; then BASE_PY="\$(command -v python)"; fi
                            if [ -z "\$BASE_PY" ]; then echo "[ERROR] Python 3.10+ not found on agent PATH."; exit 1; fi
                            echo "[INFO] Using Python: \$BASE_PY"
                            "\$BASE_PY" --version
                            echo "\$BASE_PY" > python_exe.txt
                        """,
                        """
                            @echo off
                            setlocal EnableDelayedExpansion
                            set "BASE_PY="
                            for /f "delims=" %%i in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "BASE_PY=%%i"
                            if not defined BASE_PY for /f "delims=" %%i in ('where python 2^>nul') do if not defined BASE_PY set "BASE_PY=%%i"
                            if not defined BASE_PY (echo [ERROR] Python 3.10+ not found on agent PATH. & exit /b 1)
                            echo [INFO] Using Python: !BASE_PY!
                            "!BASE_PY!" --version
                            echo !BASE_PY!> python_exe.txt
                            endlocal
                        """
                    )
                    env.RESOLVED_PYTHON = readFile('python_exe.txt').trim()
                    echo "Resolved Python: ${env.RESOLVED_PYTHON}"
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    runShell(
                        """
                            "${env.RESOLVED_PYTHON}" -m venv ${env.VENV_DIR}
                            ${env.VENV_DIR}/bin/python -m pip install --upgrade pip
                            ${env.VENV_DIR}/bin/python -m pip install -r requirements.txt
                            ${env.VENV_DIR}/bin/python -m pip install -r requirements-ci.txt
                        """,
                        """
                            "${env.RESOLVED_PYTHON}" -m venv %VENV_DIR%
                            %VENV_DIR%\\Scripts\\python -m pip install --upgrade pip
                            %VENV_DIR%\\Scripts\\python -m pip install -r requirements.txt
                            %VENV_DIR%\\Scripts\\python -m pip install -r requirements-ci.txt
                        """
                    )
                }
            }
        }

        stage('Download Extension') {
            steps {
                script {
                    runShell(
                        '${VENV_DIR}/bin/python download_extension.py',
                        '%VENV_DIR%\\Scripts\\python download_extension.py'
                    )
                }
            }
        }

        stage('Prepare Report Directories') {
            steps {
                script {
                    echo 'Clearing previous report artifacts for a fresh run.'
                    runShell(
                        '''
                            rm -rf test-results allure-results allure-report jenkins-chrome-profile || true
                            mkdir -p test-results allure-results
                        ''',
                        '''
                            if exist test-results rmdir /s /q test-results
                            if exist allure-results rmdir /s /q allure-results
                            if exist allure-report rmdir /s /q allure-report
                    if exist jenkins-chrome-profile rmdir /s /q jenkins-chrome-profile
                            mkdir test-results
                            mkdir allure-results
                        '''
                    )
                }
            }
        }

        stage('Static Validation') {
            steps {
                script {
                    def effectiveCfg = getEffectiveRunConfig()
                    validateRuntimeParameters(effectiveCfg.infraRetryCount as String)
                    def selectedTestFiles = getAllTestCaseFiles()
                    if (effectiveCfg.runSmokeOnly) {
                        echo 'Smoke mode enabled: validating 8 critical tests (-m smoke).'
                        runPytest('--version')
                        runPytest('--collect-only -q -m smoke')
                    } else {
                        echo "Full suite mode: validating ${selectedTestFiles.size()} test files."
                        runPytest('--version')
                        runPytest("--collect-only -q ${selectedTestFiles.join(' ')}")
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def effectiveCfg = getEffectiveRunConfig()
                    def selectedTestFiles = getAllTestCaseFiles()
                    def runCmd = buildPytestCommand(
                        selectedTestFiles,
                        effectiveCfg.runAllure as boolean,
                        effectiveCfg.infraRetryCount as String,
                        effectiveCfg.runSmokeOnly as boolean
                    )
                    echo "Test mode: ${effectiveCfg.runSmokeOnly ? 'SMOKE (8 tests)' : "FULL (${selectedTestFiles.size()} files)"}"
                    echo "Pytest command: pytest ${runCmd}"

                    withCredentials([usernamePassword(
                        credentialsId: "${params.DAKOTA_CREDENTIALS_ID}",
                        usernameVariable: 'DAKOTA_USERNAME',
                        passwordVariable: 'DAKOTA_PASSWORD'
                    )]) {
                        catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                            runPytest(runCmd)
                        }
                    }
                }
            }
        }

        stage('Publish Reports') {
            steps {
                script {
                    def effectiveCfg = getEffectiveRunConfig()
                    if (fileExists(env.PYTEST_JUNIT)) {
                        junit testResults: env.PYTEST_JUNIT, allowEmptyResults: true
                    }

                    try {
                        publishHTML(target: [
                            reportName: 'Pytest HTML Report',
                            reportDir: 'test-results',
                            reportFiles: 'report.html',
                            keepAll: true,
                            alwaysLinkToLastBuild: true,
                            allowMissing: true
                        ])
                    } catch (MissingMethodException ex) {
                        echo 'HTML Publisher plugin not installed; skipping publishHTML step.'
                    }

                    if (effectiveCfg.runAllure && fileExists(env.ALLURE_DIR)) {
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: env.ALLURE_DIR]],
                            reportName: 'Allure Report'
                        ])
                    } else if (effectiveCfg.runAllure) {
                        echo "Skipping Allure publish: ${env.ALLURE_DIR} directory not found."
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                def effectiveCfg = getEffectiveRunConfig()
                logTestSummaryToConsole('Post pipeline summary')
                if (fileExists('test-results')) {
                    archiveArtifacts artifacts: 'test-results/**', allowEmptyArchive: true
                }
                if (fileExists('allure-results')) {
                    archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
                }
                if (effectiveCfg.sendEmail) {
                    sendEmailNotification(
                        currentBuild.currentResult ?: 'UNKNOWN',
                        effectiveCfg.defaultEmail as String,
                        effectiveCfg.additionalEmails as String
                    )
                }
            }
        }
    }
}

// def isScheduledBuild() {
//     try {
//         def timerCauses = currentBuild?.getBuildCauses('hudson.triggers.TimerTrigger$TimerTriggerCause') ?: []
//         if (!timerCauses.isEmpty()) {
//             return true
//         }
//         def genericCauses = currentBuild?.getBuildCauses() ?: []
//         return genericCauses.any { cause ->
//             def cls = cause?._class ?: ''
//             return cls.contains('TimerTriggerCause')
//         }
//     } catch (Exception ignored) {
//         return false
//     }
// }

def getEffectiveRunConfig() {
    // def scheduled = isScheduledBuild()
    return [
        scheduledBuild   : false,
        additionalEmails : (params.ADDITIONAL_EMAILS as String),
        // additionalEmails : scheduled
        //     ? 'omer.shafiq@rolustech.net,imad.ali@rolustech.com,schal.hasnain@rolustech.com,faseeh.ahmad@rolustech.com,hina.siddiqui@rolustech.com'
        //     : (params.ADDITIONAL_EMAILS as String),
        defaultEmail     : (params.DEFAULT_EMAIL as String),
        // defaultEmail     : scheduled
        //     ? 'pstanley@dakota.com'
        //     : (params.DEFAULT_EMAIL as String),
        infraRetryCount  : params.INFRA_RETRY_COUNT as String,
        runSmokeOnly     : params.RUN_SMOKE_ONLY as boolean,
        runAllure        : params.RUN_ALLURE as boolean,
        sendEmail        : params.SEND_EMAIL as boolean,
    ]
}

def shellQuotePytestArgs(List parts) {
    parts.collect { arg ->
        if (!arg.contains(' ')) {
            return arg
        }
        return '"' + arg.replace('"', '""') + '"'
    }.join(' ')
}

def buildPytestCommand(
    List selectedTestFiles,
    boolean runAllure,
    String infraRetryCount,
    boolean runSmokeOnly = false
) {
    def allureArgs = runAllure
        ? ["--alluredir=${env.ALLURE_DIR}", '--clean-alluredir']
        : []
    def parts = []

    parts << '-vv'
    parts << '-ra'
    parts << '--tb=short'
    parts << '--color=no'
    parts << '-o'
    parts << 'console_output_style=progress'
    parts.addAll(allureArgs)

    def retries = 0
    try {
        retries = Math.max((infraRetryCount ?: '0').trim() as int, 0)
    } catch (Exception ignored) {
        retries = 1
    }

    if (retries > 0) {
        parts << "--reruns=${retries}"
        parts << '--reruns-delay=2'
        parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?TimeoutException'
        parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?NoSuchElementException'
        parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?StaleElementReferenceException'
        parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?ElementClickInterceptedException'
        parts << '--only-rerun=(selenium\\.common\\.exceptions\\.)?WebDriverException'
        parts << '--only-rerun=SessionNotCreatedException'
        parts << '--only-rerun=urllib3\\.exceptions\\.ReadTimeoutError'
        parts << '--only-rerun=ReadTimeoutError'
        parts << '--only-rerun=HTTPConnectionPool\\(host='
        parts << '--only-rerun=Read\\s+timed\\s+out'
        parts << '--only-rerun=TimeoutError'
        parts << '--only-rerun=timed\\s+out'
        parts << '--only-rerun=disconnected:\\s+not\\s+connected\\s+to\\s+DevTools'
        parts << '--only-rerun=chrome\\s+not\\s+reachable'
        parts << '--only-rerun=ERR_CONNECTION_RESET'
    }

    parts << "--junitxml=${env.PYTEST_JUNIT}"
    parts << "--html=${env.PYTEST_HTML}"
    parts << '--self-contained-html'
    parts << '--json-report'
    parts << "--json-report-file=${env.PYTEST_JSON}"
    if (runSmokeOnly) {
        parts << '-m'
        parts << 'smoke'
    } else if (selectedTestFiles && !selectedTestFiles.isEmpty()) {
        parts.addAll(selectedTestFiles)
    }

    return shellQuotePytestArgs(parts)
}

def validateRuntimeParameters(String infraRetryCount) {
    def rawRetry = (infraRetryCount ?: '').trim()
    if (!(rawRetry ==~ /^\d+$/)) {
        error("INFRA_RETRY_COUNT must be a non-negative integer, but got '${infraRetryCount}'.")
    }
}

def getAllTestCaseFiles() {
    def orderedTests = [
        'test_dakota_extension_installation',
        'test_login_to_dakota',
        'test_dakota_search_results',
        'test_dakota_search_scroll',
        'test_dakota_search_load_more',
        'test_dakota_company_details',
        'test_dakota_company_general_tab',
        'test_dakota_company_contacts_count',
        'test_dakota_company_account_overview',
        'test_dakota_company_general_tab_type',
        'test_dakota_company_general_tab_metro_area',
        'test_dakota_company_general_tab_website',
        'test_dakota_company_general_tab_linkedin_url',
        'test_dakota_company_general_tab_billing_address',
        'test_dakota_company_investors_tab',
        'test_dakota_company_investment_details_tab',
        'test_dakota_company_platform_details_tab',
        'test_dakota_investors_tab_results',
        'test_dakota_investors_tab_investor_count',
        'test_dakota_investors_tab_load_more_button',
        'test_dakota_investors_tab_load_more_displays_more',
        'test_dakota_investors_tab_investor_metro_areas',
        'test_dakota_investment_details_tab_details',
        'test_dakota_investment_details_tab_geography',
        'test_dakota_investment_details_tab_industry',
        'test_dakota_investment_details_tab_check_size',
        'test_dakota_platform_details_tab_platform_description',
        'test_dakota_contacts_tab_results',
        'test_dakota_contacts_tab_contact_count',
        'test_dakota_contacts_tab_load_more_button',
        'test_dakota_contacts_tab_load_more_displays_more',
        'test_dakota_contacts_tab_contact_roles',
        'test_dakota_contacts_tab_contact_urls',
        'test_dakota_contacts_tab_contact_emails',
        'test_dakota_contacts_tab_search_results',
        'test_dakota_contacts_tab_contact_details',
        'test_dakota_contacts_tab_contact_type',
        'test_dakota_contacts_tab_contact_metro_area',
        'test_dakota_contacts_tab_contact_phone',
        'test_dakota_contacts_tab_contact_detail_email',
        'test_dakota_contacts_tab_contact_detail_linkedin_url',
        'test_dakota_contacts_tab_go_back_to_contact_list',
        'test_dakota_linkedin_company_auto_search',
    ]
    return orderedTests.collect { "tests/${it}.py" }
}

def runShell(String unixCommand, String windowsCommand) {
    if (isUnix()) {
        sh(unixCommand)
    } else {
        bat(windowsCommand)
    }
}

def runPytest(String args) {
    runShell(
        """
            ${env.VENV_DIR}/bin/python -m pytest ${args}
        """,
        """
            %VENV_DIR%\\Scripts\\python -m pytest ${args}
        """
    )
}

def getTestStatistics() {
    def stats = [total: 0, passed: 0, failed: 0, skipped: 0]
    def junitPath = env.PYTEST_JUNIT ?: 'test-results/pytest.xml'
    def jsonSnapshot = getFinalOutcomesFromPytestJson()

    if (jsonSnapshot.hasData as boolean) {
        return jsonSnapshot.stats as Map
    }

    if (fileExists(junitPath)) {
        try {
            def xmlText = readFile(junitPath)
            def tests = extractIntFromXmlAttribute(xmlText, 'tests')
            def failures = extractIntFromXmlAttribute(xmlText, 'failures')
            def errors = extractIntFromXmlAttribute(xmlText, 'errors')
            def skipped = extractIntFromXmlAttribute(xmlText, 'skipped')
            def passed = Math.max(tests - failures - errors - skipped, 0)

            stats.total = tests
            stats.failed = failures + errors
            stats.skipped = skipped
            stats.passed = passed
            echo "Using JUnit fallback stats -> total:${stats.total}, passed:${stats.passed}, failed:${stats.failed}, skipped:${stats.skipped}"
        } catch (Exception ex) {
            echo "Could not parse JUnit XML fallback: ${ex.message}"
        }
    } else {
        echo "JUnit XML report not found at ${junitPath}; no fallback stats available."
    }

    return stats
}

def getFailedTestNames() {
    def jsonSnapshot = getFinalOutcomesFromPytestJson()
    if (jsonSnapshot.hasData as boolean) {
        return (jsonSnapshot.failedTests ?: []) as List
    }

    def failures = []
    def junitPath = env.PYTEST_JUNIT ?: 'test-results/pytest.xml'
    if (!fileExists(junitPath)) {
        return failures
    }

    try {
        def xmlText = readFile(junitPath)
        def matcher = (xmlText =~ /(?si)<testcase\b([^>]*)>(?:(?!<\/testcase>).)*<(failure|error)\b/)
        while (matcher.find()) {
            def attrs = matcher.group(1) ?: ''
            def name = extractTestNameFromAttrs(attrs)
            if (name) {
                failures << name
            }
        }
    } catch (Exception ex) {
        echo "Could not parse failed test names from JUnit XML: ${ex.message}"
    }

    return failures.unique()
}

def extractTestNameFromAttrs(String attrs) {
    def nameMatcher = (attrs =~ /\bname=(["'])(.*?)\1/)
    def classMatcher = (attrs =~ /\bclassname=(["'])(.*?)\1/)
    def name = nameMatcher.find() ? nameMatcher.group(2)?.trim() : ''
    def className = classMatcher.find() ? classMatcher.group(2)?.trim() : ''

    def candidate = name
    if ((!candidate || !candidate.startsWith('test_')) && className) {
        candidate = className.tokenize('.').last()
    }
    return candidate
}

def getFinalOutcomesFromPytestJson() {
    def reportPath = env.PYTEST_JSON ?: 'test-results/report.json'
    def emptyStats = [total: 0, passed: 0, failed: 0, skipped: 0]
    def result = [hasData: false, stats: emptyStats, failedTests: []]

    if (!fileExists(reportPath)) {
        echo "Pytest JSON report not found at ${reportPath}; trying JUnit fallback."
        return result
    }

    try {
        def jsonText = readFile(reportPath)
        def finalOutcomeByNodeId = [:]

        def testMatcher = (jsonText =~ /"nodeid"\s*:\s*"((?:\\.|[^"\\])*)".*?"outcome"\s*:\s*"((?:\\.|[^"\\])*)"/)
        while (testMatcher.find()) {
            def nodeId = (testMatcher.group(1) ?: '')
                .replaceAll(/\\\//, '/')
                .replaceAll(/\\"/, '"')
                .trim()
            def outcome = (testMatcher.group(2) ?: '').trim().toLowerCase()
            if (!nodeId || !outcome) {
                continue
            }
            if (outcome in ['rerun', 're-run']) {
                continue
            }
            if (outcome == 'error') {
                outcome = 'failed'
            }
            if (outcome in ['xfailed', 'xpassed']) {
                outcome = 'skipped'
            }
            if (!(outcome in ['passed', 'failed', 'skipped'])) {
                continue
            }
            finalOutcomeByNodeId[nodeId] = outcome
        }

        def parseSummaryInt = { String key ->
            def m = (jsonText =~ /"summary"\s*:\s*\{(?s).*?"${java.util.regex.Pattern.quote(key)}"\s*:\s*(\d+)/)
            return m.find() ? (m.group(1) ?: '0') as int : 0
        }
        def collected = parseSummaryInt('collected')

        if (!finalOutcomeByNodeId.isEmpty()) {
            def passed = finalOutcomeByNodeId.findAll { _, status -> status == 'passed' }.size()
            def failed = finalOutcomeByNodeId.findAll { _, status -> status == 'failed' }.size()
            def skipped = finalOutcomeByNodeId.findAll { _, status -> status == 'skipped' }.size()
            def total = passed + failed + skipped
            if (collected > 0 && total > collected) {
                def normFailed = Math.min(failed, collected)
                def remainingAfterFailed = Math.max(collected - normFailed, 0)
                def normSkipped = Math.min(skipped, remainingAfterFailed)
                def normPassed = Math.max(collected - normFailed - normSkipped, 0)
                passed = normPassed
                failed = normFailed
                skipped = normSkipped
                total = collected
            }
            def failedTests = finalOutcomeByNodeId
                .findAll { _, status -> status == 'failed' }
                .collect { nodeId, _ -> extractDisplayNameFromNodeId(nodeId as String) }
                .findAll { it }
                .unique()
            return [
                hasData: true,
                stats: [total: total, passed: passed, failed: failed, skipped: skipped],
                failedTests: failedTests
            ]
        }

        def passed = parseSummaryInt('passed')
        def failed = parseSummaryInt('failed') + parseSummaryInt('error')
        def skipped = parseSummaryInt('skipped') + parseSummaryInt('xfailed') + parseSummaryInt('xpassed')
        def total = passed + failed + skipped
        if (collected > 0 && total > collected) {
            def normFailed = Math.min(failed, collected)
            def remainingAfterFailed = Math.max(collected - normFailed, 0)
            def normSkipped = Math.min(skipped, remainingAfterFailed)
            def normPassed = Math.max(collected - normFailed - normSkipped, 0)
            passed = normPassed
            failed = normFailed
            skipped = normSkipped
            total = collected
        }
        if (total > 0) {
            return [hasData: true, stats: [total: total, passed: passed, failed: failed, skipped: skipped], failedTests: []]
        }
    } catch (Exception ex) {
        echo "Could not parse pytest JSON report: ${ex.message}"
    }

    return result
}

def extractDisplayNameFromNodeId(String nodeId) {
    def value = (nodeId ?: '').trim()
    if (!value) {
        return value
    }

    if (value.contains('::')) {
        value = value.tokenize('::').last()
    } else if (value.contains('/')) {
        value = value.tokenize('/').last()
    } else if (value.contains('\\')) {
        value = value.tokenize('\\').last()
    }
    return value.replaceFirst(/\[.*\]$/, '')
}

def extractIntFromXmlAttribute(String xmlText, String attr) {
    if (!xmlText?.trim()) {
        return 0
    }
    def matcher = (xmlText =~ /${java.util.regex.Pattern.quote(attr)}\s*=\s*["'](\d+)["']/)
    if (matcher.find()) {
        return (matcher.group(1) ?: '0') as int
    }
    return 0
}

def logTestSummaryToConsole(String label = 'Test summary') {
    def stats = getTestStatistics()
    echo """
================ ${label} ================
Total   : ${stats.total}
Passed  : ${stats.passed}
Failed  : ${stats.failed}
Skipped : ${stats.skipped}
==========================================
""".stripIndent()
}

def resolveBuildStatusLabel(String buildStatus, Map stats, List failedTests) {
    def actualStatus = currentBuild.result ?: buildStatus
    if (!(actualStatus in ['FAILURE', 'ABORTED'])) {
        if (stats.total == 0) {
            actualStatus = 'UNSTABLE'
        } else if (stats.failed > 0) {
            actualStatus = 'FAILURE'
        } else {
            actualStatus = 'SUCCESS'
        }
    }
    return actualStatus
}

def buildStatusTheme(String status) {
    switch (status) {
        case 'SUCCESS':
            return [
                label      : 'All Checks Passed',
                badgeBg    : '#10261c',
                badgeText  : '#8ef0c2',
                badgeBorder: '#2f6f52',
                accent     : '#2dd4a8',
                accentSoft : '#d9f8ec',
                ink        : '#10131a',
                heroStart  : '#10131a',
                heroEnd    : '#1f2a44',
                glow       : '#2dd4a8',
            ]
        case 'UNSTABLE':
            return [
                label      : 'Build Completed With Warnings',
                badgeBg    : '#2a2010',
                badgeText  : '#f6d58b',
                badgeBorder: '#8a6a2d',
                accent     : '#d4a017',
                accentSoft : '#fff4d6',
                ink        : '#10131a',
                heroStart  : '#10131a',
                heroEnd    : '#3a2d14',
                glow       : '#d4a017',
            ]
        case 'FAILURE':
            return [
                label      : 'Build Failed',
                badgeBg    : '#2a1218',
                badgeText  : '#ffb4c0',
                badgeBorder: '#8a3040',
                accent     : '#ef5f7a',
                accentSoft : '#ffe4e8',
                ink        : '#10131a',
                heroStart  : '#10131a',
                heroEnd    : '#3a1820',
                glow       : '#ef5f7a',
            ]
        default:
            return [
                label      : 'Build Finished',
                badgeBg    : '#141c2e',
                badgeText  : '#b8c9ff',
                badgeBorder: '#3d4f78',
                accent     : '#7aa2ff',
                accentSoft : '#e8efff',
                ink        : '#10131a',
                heroStart  : '#10131a',
                heroEnd    : '#24314f',
                glow       : '#7aa2ff',
            ]
    }
}

def sendEmailNotification(String buildStatus, String defaultEmail, String additionalEmails) {
    def stats = getTestStatistics()
    def failedTests = getFailedTestNames()
    def actualStatus = resolveBuildStatusLabel(buildStatus, stats, failedTests)
    def theme = buildStatusTheme(actualStatus)

    def recipients = collectRecipientEmails(defaultEmail, additionalEmails)
    if (recipients.isEmpty()) {
        echo 'No email recipients configured; skipping email notification.'
        return
    }

    def jobUrl = env.BUILD_URL ?: ''
    def allureUrl = "${jobUrl}allure"
    def htmlUrl = "${jobUrl}Pytest_20HTML_20Report"
    def durationString = (currentBuild.durationString ?: 'N/A').replace(' and counting', '')
    def passRate = stats.total > 0 ? ((stats.passed * 100) / stats.total) as int : 0
    def runDate = new Date().format('MMMM d, yyyy')

    def passRateColor = passRate >= 90 ? '#4ade80' : (passRate >= 70 ? '#fbbf24' : '#f87171')
    def allureAvailable = fileExists(env.ALLURE_DIR ?: 'allure-results')
    def allureButtonHtml = allureAvailable
        ? "<a href=\"${allureUrl}\" style=\"display:inline-block;background:#ffffff;color:#0f172a;text-decoration:none;padding:10px 16px;border-radius:10px;font-size:11px;font-weight:900;letter-spacing:0.7px;box-shadow:0 8px 16px rgba(0,0,0,0.2);\">OPEN REPORT</a>"
        : '<span style="display:inline-block;background:rgba(255,255,255,0.16);color:#ffffff;padding:10px 16px;border-radius:10px;font-size:10px;font-weight:800;">REPORT NOT AVAILABLE</span>'
    def htmlButtonHtml = fileExists(env.PYTEST_HTML ?: 'test-results/report.html')
        ? "<a href=\"${htmlUrl}\" style=\"display:inline-block;margin-top:10px;background:rgba(255,255,255,0.14);color:#ffffff;text-decoration:none;padding:9px 14px;border-radius:10px;font-size:10px;font-weight:800;letter-spacing:0.6px;border:1px solid rgba(255,255,255,0.22);\">PYTEST HTML</a>"
        : ''

    def cleanedFailedTests = failedTests.collect { normalizeFailedTestNameToLabel(it ?: '') }.findAll { it }

    def corporateIssueList = { List items, String accentColor, String bgColor, String emptyMessage ->
        if (!items) {
            return """
            <div style="padding:14px 16px;font-size:13px;font-weight:700;color:#15803d;background:#ecfaf3;border:1px solid #c9efdc;border-radius:12px;text-align:center;line-height:1.5;">
              ${emptyMessage}
            </div>
            """.stripIndent()
        }
        items.collect { item ->
            """
            <div style="margin:0 0 8px;padding:11px 14px;background:${bgColor};border:1px solid #dbe3ef;border-left:4px solid ${accentColor};border-radius:12px;font-size:12px;font-weight:700;color:#0f172a;line-height:1.5;">${item}</div>
            """.stripIndent()
        }.join('')
    }

    def failedTestSummary = corporateIssueList(
        cleanedFailedTests,
        '#b91c1c',
        '#fef2f2',
        'No failed tests reported.'
    )

    def subject = "Dakota Chrome Extension UI | ${runDate}"

    def body = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dakota Chrome Extension UI Report</title>
  </head>
  <body style="margin:0;padding:0;background:#e8edf5;font-family:'Segoe UI',Arial,'Trebuchet MS',sans-serif;">

    <table width="100%" cellpadding="0" cellspacing="0" style="padding:28px 12px;background:linear-gradient(160deg,#dfe8f8 0%,#f4f7fb 55%,#eef2f7 100%);">
      <tr>
        <td align="center">

          <table width="100%" cellpadding="0" cellspacing="0" style="max-width:680px;background:#ffffff;border-radius:28px;overflow:hidden;box-shadow:0 28px 64px rgba(15,23,42,0.16);border:1px solid #e3eaf3;">

            <tr>
              <td style="padding:0;background:linear-gradient(135deg,#0b1220 0%,#1e3a8a 52%,#0ea5e9 100%);">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <td style="padding:30px 28px 22px;">
                      <div style="font-size:11px;color:#93c5fd;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;margin-bottom:8px;">Automation Report</div>
                      <h1 style="margin:0;color:#ffffff;font-size:28px;line-height:1.15;font-weight:900;letter-spacing:-0.3px;">Dakota Chrome Extension UI Test Results</h1>
                    </td>
                  </tr>
                  <tr>
                    <td style="height:3px;background:linear-gradient(90deg,#0ea5e9,#38bdf8,#818cf8);font-size:0;line-height:0;">&nbsp;</td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="padding:18px 18px 8px;">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <td width="25%" style="padding:4px;">
                      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;border:1px solid #dbe3ef;border-radius:16px;box-shadow:0 4px 14px rgba(15,23,42,0.04);">
                        <tr><td style="padding:16px 10px;text-align:center;">
                          <div style="font-size:10px;color:#64748b;font-weight:800;letter-spacing:0.9px;">TOTAL</div>
                          <div style="margin-top:8px;font-size:30px;font-weight:900;color:#0f172a;line-height:1;">${stats.total}</div>
                        </td></tr>
                      </table>
                    </td>
                    <td width="25%" style="padding:4px;">
                      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0fdf7;border:1px solid #bbf7d0;border-radius:16px;box-shadow:0 4px 14px rgba(21,128,61,0.08);">
                        <tr><td style="padding:16px 10px;text-align:center;">
                          <div style="font-size:10px;color:#15803d;font-weight:800;letter-spacing:0.9px;">PASSED</div>
                          <div style="margin-top:8px;font-size:30px;font-weight:900;color:#15803d;line-height:1;">${stats.passed}</div>
                        </td></tr>
                      </table>
                    </td>
                    <td width="25%" style="padding:4px;">
                      <table width="100%" cellpadding="0" cellspacing="0" style="background:#fef2f2;border:1px solid #fecaca;border-radius:16px;box-shadow:0 4px 14px rgba(185,28,28,0.06);">
                        <tr><td style="padding:16px 10px;text-align:center;">
                          <div style="font-size:10px;color:#b91c1c;font-weight:800;letter-spacing:0.9px;">FAILED</div>
                          <div style="margin-top:8px;font-size:30px;font-weight:900;color:#b91c1c;line-height:1;">${stats.failed}</div>
                        </td></tr>
                      </table>
                    </td>
                    <td width="25%" style="padding:4px;">
                      <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f3ff;border:1px solid #ddd6fe;border-radius:16px;box-shadow:0 4px 14px rgba(124,58,237,0.07);">
                        <tr><td style="padding:16px 10px;text-align:center;">
                          <div style="font-size:10px;color:#7c3aed;font-weight:800;letter-spacing:0.9px;">SKIPPED</div>
                          <div style="margin-top:8px;font-size:30px;font-weight:900;color:#7c3aed;line-height:1;">${stats.skipped}</div>
                        </td></tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="padding:8px 18px 20px;">
                <table width="100%" cellpadding="0" cellspacing="0">
                  <tr>
                    <td width="50%" height="232" valign="top" style="padding-right:5px;">
                      <table width="100%" height="232" cellpadding="0" cellspacing="0" style="border:1px solid #3f3f46;border-radius:18px;overflow:hidden;background:#0f0f10;">
                        <tr>
                          <td height="48" style="padding:0 16px;background:linear-gradient(90deg,#18181b 0%,#27272a 100%);border-bottom:1px solid #3f3f46;color:#f4f4f5;font-size:14px;font-weight:900;vertical-align:middle;line-height:48px;">Execution Details</td>
                        </tr>
                        <tr>
                          <td height="184" valign="middle" style="padding:12px 14px;background:#1a1a1a;">
                            <table width="100%" height="160" cellpadding="0" cellspacing="0" style="background:linear-gradient(180deg,#2a2a2a 0%,#1a1a1a 100%);border:1px solid #52525b;border-radius:14px;box-shadow:0 10px 28px rgba(0,0,0,0.45);">
                              <tr>
                                <td height="160" valign="middle" style="padding:14px 14px 10px;text-align:center;">
                                  <div style="font-size:10px;color:#a1a1aa;font-weight:800;letter-spacing:1.4px;text-transform:uppercase;">Pass Rate</div>
                                  <div style="margin:8px 0 12px;font-size:42px;font-weight:900;line-height:1;color:${passRateColor};text-shadow:0 2px 12px rgba(0,0,0,0.35);">${passRate}<span style="font-size:18px;color:#d4d4d8;">%</span></div>
                                  <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:10px;">
                                    <tr>
                                      <td style="height:11px;background:#333333;border-radius:999px;font-size:0;line-height:0;border:1px solid #52525b;">
                                        <div style="width:${passRate}%;max-width:100%;height:9px;margin:1px;background:linear-gradient(90deg,#6366f1,#22d3ee,#4ade80);border-radius:999px;"></div>
                                      </td>
                                    </tr>
                                  </table>
                                  <table width="100%" cellpadding="0" cellspacing="0" style="background:#2d2d2d;border:1px solid #52525b;border-radius:10px;">
                                    <tr>
                                      <td style="padding:10px 12px;font-size:11px;font-weight:800;color:#a1a1aa;">Duration</td>
                                      <td align="right" style="padding:10px 12px;font-size:12px;font-weight:900;color:#fafafa;">${durationString}</td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>

                    <td width="50%" height="232" valign="top" style="padding-left:5px;">
                      <table width="100%" height="232" cellpadding="0" cellspacing="0" style="border:1px solid #c7d2fe;border-radius:18px;overflow:hidden;background:#ffffff;">
                        <tr>
                          <td height="48" style="padding:0 16px;background:linear-gradient(90deg,#312e81 0%,#1d4ed8 48%,#0891b2 100%);color:#ffffff;font-size:14px;font-weight:900;vertical-align:middle;line-height:48px;">Allure Report</td>
                        </tr>
                        <tr>
                          <td height="184" valign="middle" style="padding:12px 14px;background:linear-gradient(160deg,#020617 0%,#0f172a 45%,#1d4ed8 100%);">
                            <table width="100%" height="160" cellpadding="0" cellspacing="0">
                              <tr>
                                <td height="160" valign="middle" style="padding:0 4px;">
                                  <div style="color:#ffffff;font-size:20px;line-height:1.25;font-weight:900;">Test Evidence</div>
                                  <div style="margin-top:8px;color:#cbd5e1;font-size:12px;line-height:1.55;">
                                    Analytics, screenshots, logs, and validation details.
                                  </div>
                                  <div style="margin-top:16px;">${allureButtonHtml}</div>
                                  <div style="margin-top:8px;">${htmlButtonHtml}</div>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            ${cleanedFailedTests ? """
            <tr>
              <td style="padding:0 18px 20px;">
                <table width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border:1px solid #fecaca;border-radius:18px;overflow:hidden;">
                  <tr>
                    <td style="padding:14px 16px;background:#fef2f2;color:#b91c1c;font-size:13px;font-weight:900;">Failed Tests</td>
                  </tr>
                  <tr>
                    <td style="padding:14px 16px;">${failedTestSummary}</td>
                  </tr>
                </table>
              </td>
            </tr>
            """ : ''}

            <tr>
              <td style="background:#0a0a0a;padding:14px 18px;text-align:center;">
                <span style="color:#f8fafc;font-size:11px;font-weight:800;letter-spacing:0.3px;">Dakota Marketplace Automation</span>
              </td>
            </tr>

          </table>

        </td>
      </tr>
    </table>

  </body>
</html>
"""

    def baseArgs = [
        subject: subject,
        body: body,
        mimeType: 'text/html',
        attachLog: false,
        compressLog: false
    ]

    def recipientList = recipients.join(', ')
    echo "Sending email to: ${recipientList}"

    try {
        emailext(baseArgs + [to: recipientList])
    } catch (Exception ex) {
        echo "Combined email send failed: ${ex.getMessage()}"
        echo 'Falling back to one-by-one recipient delivery.'
        recipients.each { recipient ->
            try {
                echo "Sending fallback email to: ${recipient}"
                emailext(baseArgs + [to: recipient])
            } catch (Exception innerEx) {
                echo "Failed to send email to ${recipient}: ${innerEx.getMessage()}"
            }
        }
    }
}

def normalizeFailedTestNameToLabel(String testName) {
    def value = (testName ?: '').trim()
    if (!value) {
        return value
    }

    value = value
        .replaceFirst(/^.*::/, '')
        .replaceFirst(/^.*[\\\/]/, '')
        .replaceFirst(/\.py$/, '')
    if (value.contains('.') && value.tokenize('.').last().startsWith('test_')) {
        value = value.tokenize('.').last()
    }

    def labelMap = [
        'test_dakota_extension_installation'                       : 'Extension Installation',
        'test_login_to_dakota'                                     : 'Portal And Extension Login',
        'test_dakota_search_results'                               : 'Search Results',
        'test_dakota_search_scroll'                                : 'Search Scroll',
        'test_dakota_search_load_more'                             : 'Search Load More',
        'test_dakota_company_details'                              : 'Company Details',
        'test_dakota_company_general_tab'                            : 'Company General Tab',
        'test_dakota_company_contacts_count'                         : 'Company Contacts Count',
        'test_dakota_company_account_overview'                     : 'Company Account Overview',
        'test_dakota_company_general_tab_type'                       : 'General Tab Company Type',
        'test_dakota_company_general_tab_metro_area'               : 'General Tab Metro Area',
        'test_dakota_company_general_tab_website'                    : 'General Tab Website',
        'test_dakota_company_general_tab_linkedin_url'               : 'General Tab LinkedIn URL',
        'test_dakota_company_general_tab_billing_address'            : 'General Tab Billing Address',
        'test_dakota_company_investors_tab'                          : 'Company Investors Tab',
        'test_dakota_company_investment_details_tab'                 : 'Company Investment Details Tab',
        'test_dakota_company_platform_details_tab'                   : 'Company Platform Details Tab',
        'test_dakota_investors_tab_results'                          : 'Investors Tab Results',
        'test_dakota_investors_tab_investor_count'                   : 'Investors Tab Count',
        'test_dakota_investors_tab_load_more_button'                 : 'Investors Load More Button',
        'test_dakota_investors_tab_load_more_displays_more'          : 'Investors Load More Displays More',
        'test_dakota_investors_tab_investor_metro_areas'             : 'Investors Metro Areas',
        'test_dakota_investment_details_tab_details'                 : 'Investment Details',
        'test_dakota_investment_details_tab_geography'               : 'Investment Geography',
        'test_dakota_investment_details_tab_industry'                : 'Investment Industry',
        'test_dakota_investment_details_tab_check_size'              : 'Investment Check Size',
        'test_dakota_platform_details_tab_platform_description'      : 'Platform Description',
        'test_dakota_contacts_tab_results'                           : 'Contacts Tab Results',
        'test_dakota_contacts_tab_contact_count'                     : 'Contacts Tab Count',
        'test_dakota_contacts_tab_load_more_button'                  : 'Contacts Load More Button',
        'test_dakota_contacts_tab_load_more_displays_more'           : 'Contacts Load More Displays More',
        'test_dakota_contacts_tab_contact_roles'                     : 'Contact Roles',
        'test_dakota_contacts_tab_contact_urls'                      : 'Contact URLs',
        'test_dakota_contacts_tab_contact_emails'                    : 'Contact Emails',
        'test_dakota_contacts_tab_search_results'                    : 'Contacts Search Results',
        'test_dakota_contacts_tab_contact_details'                   : 'Contact Details',
        'test_dakota_contacts_tab_contact_type'                      : 'Contact Type',
        'test_dakota_contacts_tab_contact_metro_area'                : 'Contact Metro Area',
        'test_dakota_contacts_tab_contact_phone'                     : 'Contact Phone',
        'test_dakota_contacts_tab_contact_detail_email'              : 'Contact Detail Email',
        'test_dakota_contacts_tab_contact_detail_linkedin_url'       : 'Contact Detail LinkedIn URL',
        'test_dakota_contacts_tab_go_back_to_contact_list'         : 'Go Back To Contact List',
        'test_dakota_linkedin_company_auto_search'                   : 'LinkedIn Company Auto Search',
    ]
    if (labelMap.containsKey(value)) {
        return labelMap[value]
    }

    value = value
        .replaceFirst(/^test_/, '')
        .replaceFirst(/\[.*\]$/, '')

    def words = value
        .split(/_+/)
        .findAll { it?.trim() }
        .collect { it.toLowerCase().capitalize() }

    return words ? words.join(' ') : testName
}

def collectRecipientEmails(String defaultEmail, String additionalEmails) {
    def recipients = []
    def seen = [] as Set

    [defaultEmail, additionalEmails].findAll { it?.trim() }.each { source ->
        source
            .split(/[,\s;]+/)
            .collect { it.trim() }
            .findAll { it }
            .each { mail ->
                def normalized = mail.toLowerCase()
                if (!seen.contains(normalized)) {
                    seen.add(normalized)
                    recipients.add(mail)
                }
            }
    }

    echo "Email recipients resolved: ${recipients.join(', ')}"
    return recipients
}
