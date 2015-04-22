# Hermes Setup

Below describes the exact setup of the Hermes CMS for development purposes.

## Jenkins Setup
Jenkins is setup outside of the AWS Infrastructure on a Debian machine.

### Plugins

Below are the Jenkins Plugins that were installed including their version.
	
1. Amazon EC2 plugin - 1.27
1. AnsiColor - 0.4.1	
1. Build Monitor View - 1.6+build.142			
1. Build Pipeline Plugin -1 .4.7			
1. build-name-setter - 1.3			
1. CloudBees Folders Plugin - 4.7			
1. Cobertura Plugin - 1.9.7			
1. conditional-buildstep - 1.3.3	
1. Copy Artifact Plugin - 1.35			
1. Dashboard View - 2.9.4			
1. disk-usage plugin - 0.25			
1. Environment Injector Plugin - 1.91.2	
1. External Monitor Job Type Plugin - 1.4			
1. Extra Columns Plugin - 1.15			
1. GIT client plugin - 1.16.1	
1. Git Parameter Plug-In - 0.4.0			
1. GIT plugin - 2.3.5			
1. GitHub API Plugin - 1.67			
1. Github Authentication plugin - 0.20			
1. GitHub plugin - 1.11.3			
1. Green Balls - 1.14			
1. JUnit Plugin - 1.5	
1. Mailer Plugin - 1.15	
1. Multijob plugin - 1.16			
1. Parameterized Trigger plugin - 2.26		
1. Rebuilder - 1.22	
1. Release Plugin - 2.4.1	
1. Run Condition Plugin - 1.0	
1. S3 publisher plugin - 0.7			
1. SSH Agent Plugin - 1.5			
1. SSH Credentials Plugin - 1.11	
1. SSH Slaves plugin - 1.9			
1. Timestamper - 1.6			
1. Violations plugin - 0.7.11	
1. Wall Display Master Project - 0.6.2			
1. xUnit plugin - 1.94
1. Xvfb plugin - 1.0.16

### Creating the Jenkins Slave Image

The Jenkins Image is called labelled hermes-slave.

```
packer build
```

### Build Plans

There are 3 build plans as follows:

1. Branches - Branches simply do run unit tests, pylint and jshint code checking. They are done on branches that are either
    1. feature
    1. patch
    1. integration
1. Develop - Develop runs unit tests, build RPMs, bake AMIs, create cloud, integration tests, end to end tests and delete cloud. This is run when a merge commit happens on the develop branch.
1. Release - Similar to Develop it has an additional job in the build plan to generate documentation. It only runs when a merge commit is done on a release branch.

#### Branches

The order of build plans and what they do.

1. 0_Trigger_Build - The trigger build waits for a POST request from github and validates which branch the push was from. If its a valid branch then this will trigger the Branches build plan and go on to the next job.
1. 1_Code_Tests - When the trigger build has finished successfully it goes to this job which does unit tests, and linting of code (pylint, jshint). If the build is stable Github is notified with success otherwise the Pull Request fails.

#### Develop

#### Release

### The build plans

Below explains what is required to setup each build job.

#### 0_Trigger_Build

The trigger build initiates the CI plan

1. Restrict where this project can be run: Master
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. :.*/feature/.*
    1  :.*/patch/.*
    1. :.*/integration/.*
1. Build Triggers:
    1. Build when a change is pushed to GitHub
1. Build Environment:
    1. Add timestamps to the Console Output
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Set build status to "pending" on Github commit
1. Post build actions.
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Branches/1_Code_Tests
        1. Trigger when build is: Stable
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}


#### 1_Code_Tests

The code tests run the unit tests, pylint and jshint checking.

1. Discard Old Builds
    1. Max \# of builds to keep: 10
1. GitHub project: https://github.com/pmcilwaine/hermes/
1. Restrict where this project can be run
    1. Label expression: hermes-slave
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. */develop
1. Build Environment:
    1. Add timestamps to the Console Output
    1. SSH Agent
        1. Credentials: ssh agent
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Execute Shell:
        ./ci/unit_test.sh
        ./ci/run_pylint.sh
        ./ci/run_jshint.sh
    1. Inject Environment variables
        1. Properties File path: version.properties
1. Post-build Actions
    1. Publish Cobertura Coverage Report
        1. Cobertura XML report pattern: **/coverage.xml
    1. Publish JUnit test report
        1. Test report XMLs: **/junit-*.xml
        1. Health report amplification factor: 1.0
    1. Report Violations
        ![Report Violations](assets/99_hermes_setup_report_violations.png)
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Develop/2_Build_RPMs
        1. Trigger when build is: Stable
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}

#### 2_Build_RPMs

This builds all RPMs and pushes them to the yum repository.

1. Discard Old Builds
    1. Max \# of builds to keep: 10
1. GitHub project: https://github.com/pmcilwaine/hermes/
1. This build is parameterized
    1. String Parameter
        1. Name: Version
        1. Description: The version of the build.
1. Restrict where this project can be run
    1. Label expression: hermes-slave
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. */develop
1. Build Environment:
    1. Add timestamps to the Console Output
    1. SSH Agent
        1. Credentials: ssh agent
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Execute Shell:
        ./ci/build_rpms.sh -v $VERSION
    1. Execute Shell:
        ./ci/build_yumrepo.sh -v $VERSION
1. Post-build Actions
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Develop/3_Bake_AMIs
        1. Trigger when build is: Stable
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}

#### 3_Bake_AMIs

This creates new AMIs using packer and ansible.

1. Discard Old Builds
    1. Max \# of builds to keep: 10
1. GitHub project: https://github.com/pmcilwaine/hermes/
1. This build is parameterized
    1. String Parameter
        1. Name: Version
        1. Description: The version of the build.
1. Restrict where this project can be run
    1. Label expression: hermes-slave
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. */develop
1. Build Environment:
    1. Add timestamps to the Console Output
    1. SSH Agent
        1. Credentials: ssh agent
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Execute Shell:
        ./ci/bake_amis.sh -v $VERSION
1. Post-build Actions
    1. Publish Cobertura Coverage Report
        1. Cobertura XML report pattern: **/coverage.xml
    1. Publish JUnit test report
        1. Test report XMLs: **/junit-*.xml
        1. Health report amplification factor: 1.0
    1. Report Violations
        [image assets/99_hermes_setup_report_violations.png]
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Develop/4_Create_Cloud
        1. Trigger when build is: Stable
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}

#### 4_Create_Cloud

This creates a cloud to do testing in.

1. Discard Old Builds
    1. Max \# of builds to keep: 10
1. GitHub project: https://github.com/pmcilwaine/hermes/
1. This build is parameterized
    1. String Parameter
        1. Name: Version
        1. Description: The version of the build.
1. Restrict where this project can be run
    1. Label expression: hermes-slave
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. */develop
1. Build Environment:
    1. Add timestamps to the Console Output
    1. SSH Agent
        1. Credentials: ssh agent
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Execute Shell:
        ./ci/bake_amis.sh -v $VERSION
1. Post-build Actions
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Develop/5_Functional_Tests
        1. Trigger when build is: Stable
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}

#### 5_Integration_Tests

This does integration tests on the cloud.

1. Discard Old Builds
    1. Max \# of builds to keep: 10
1. GitHub project: https://github.com/pmcilwaine/hermes/
1. This build is parameterized
    1. String Parameter
        1. Name: Version
        1. Description: The version of the build.
1. Restrict where this project can be run
    1. Label expression: hermes-slave
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. */develop
1. Build Environment:
    1. Add timestamps to the Console Output
    1. SSH Agent
        1. Credentials: ssh agent
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Execute Shell:
        ./ci/integration_tests.sh -v $VERSION
1. Post-build Actions
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Develop/6_End_To_End_Tests
        1. Trigger when build is: Stable
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Develop/7_Delete_Cloud
        1. Trigger when build is: Unstable or failed but not stable
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}

#### 6_End_To_End_Tests

This does a full end to end test on the system.

1. Discard Old Builds
    1. Max \# of builds to keep: 10
1. GitHub project: https://github.com/pmcilwaine/hermes/
1. This build is parameterized
    1. String Parameter
        1. Name: Version
        1. Description: The version of the build.
1. Restrict where this project can be run
    1. Label expression: hermes-slave
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. */develop
1. Build Environment:
    1. Add timestamps to the Console Output
    1. SSH Agent
        1. Credentials: ssh agent
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Execute Shell:
        ./ci/e2e_tests.sh -v $VERSION
1. Post-build Actions
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Develop/6_End_To_End_Tests
        1. Trigger when build is: Complete (Always trigger)
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}

#### 7_Delete_Cloud

1. Discard Old Builds
    1. Max \# of builds to keep: 10
1. GitHub project: https://github.com/pmcilwaine/hermes/
1. This build is parameterized
    1. String Parameter
        1. Name: Version
        1. Description: The version of the build.
1. Restrict where this project can be run
    1. Label expression: hermes-slave
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. */develop
1. Build Environment:
    1. Add timestamps to the Console Output
    1. SSH Agent
        1. Credentials: ssh agent
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Execute Shell:
        ./ci/delete_cloud.sh -v $VERSION
1. Post-build Actions
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Trigger parameterized build on other projects
        1. Project to build: Hermes/Develop/8_Create_Documentation
        1. Trigger when build is: Stable
        1. Parameters properties from file
            1. Use properties from file: git.properties
        1. Pass-through Git commit that was built.
        1. Predefined parameters
            1. Parameters: VERSION=${VERSION}
    1. Set build status on Github commit (only on develop)

#### 8_Create_Documentation

Create documentation is only run on the release CI plan. It creates user, developer documentation.

1. Discard Old Builds
    1. Max \# of builds to keep: 10
1. GitHub project: https://github.com/pmcilwaine/hermes/
1. This build is parameterized
    1. String Parameter
        1. Name: Version
        1. Description: The version of the build.
1. Restrict where this project can be run
    1. Label expression: hermes-slave
1. SCM - Git git@github.com:pmcilwaine/hermes.git with build user git credentials
1. Branches to build:
    1. */develop
1. Build Environment:
    1. Add timestamps to the Console Output
    1. SSH Agent
        1. Credentials: ssh agent
    1. Set Build Name
        1. \#${BUILD_NUMBER}_${GIT_BRANCH}_${GIT_REVISION,length=8}
1. Build
    1. Execute Shell:
        ./ci/generate_doc.sh -v $VERSION
1. Post-build Actions
    1. Email Notification
        1. Send separate e-mails to individuals who broke the build
    1. Set build status on Github commit

## Python Setup
Development is conducted on a Mac using Python 2.7.9 in a python virtual environment using virtualenv.
