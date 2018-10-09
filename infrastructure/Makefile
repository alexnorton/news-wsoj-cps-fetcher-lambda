include ../.env
include ../.env.local

TEMPLATE=file://./stack.yml

.PHONY: create-stack
create-stack:
	aws --profile=$(CLI_PROFILE) cloudformation create-stack \
		--stack-name $(STACK_NAME) \
		--template-body $(TEMPLATE) \
		--parameters ContentApiKey=$(CONTENT_API_KEY) \
		--capabilities CAPABILITY_IAM

.PHONY: update-stack
update-stack:
	aws --profile=$(CLI_PROFILE) cloudformation update-stack \
		--stack-name $(STACK_NAME) \
		--template-body $(TEMPLATE) \
		--parameters ParameterKey=ContentApiKey,ParameterValue=$(CONTENT_API_KEY) \
		--capabilities CAPABILITY_IAM

.PHONY: delete-stack
delete-stack:
	aws --profile=$(CLI_PROFILE) cloudformation delete-stack \
		--stack-name $(STACK_NAME) \
