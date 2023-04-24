# vault-usage-parser 
  ## README and Tool is WIP
## Why
  - This tool shows the simplicity and flexibility of working with the data from the Vault Usage Metrics API.
  - The initial use case was to show "redacted" how they can do internal accounting and bill internal customers for their usage.
  - Also, the Vault auditor tool is not maintained anymore and didn't get the same improvements introduced in Vault 1.9 and higher.
  - It can also be helpful to get a quick overview of the current client count for renewals.
    - Improves trust in the built-in client count system since we don't rely on an "external tool"
    
## How does it work
### Prerequisites / Dependencies
  - `Python3`
  - `curl` _optional_ 
  - `vault` _optional_
  - `valid vault token with an appopriate policy`
    - link to policy
    

### Get Vault Usage data
- #### Option 1: Let the tool get it for you
  - Just set the ENV variables:
    - `VAULT_TOKEN` and `VAULT_ADDR` (e.g. https://localhost:8200)
   
    `export VAULT_ADDR=<vault-address> && export VAULT_TOKEN=<your-token>`
    
- #### Option 2: Manually through CLI/API/UI
  - API with curl:
    
    ```
     export VAULT_ADDR=<vault-address> && export VAULT_TOKEN=<your-token>`
    ```
    ```
     curl --header "X-Vault-Token: $VAULT_TOKEN" \
        $VAULT_ADDR/v1/sys/internal/counters/activity > output.json
    ```
    ```
     curl --header "X-Vault-Token: $VAULT_TOKEN" \
        $VAULT_ADDR/v1/sys/internal/counters/activity/monthly > ouput_monthly.json
    ```
  - Vault CLI
    ```
     export VAULT_ADDR=<vault-address> && export VAULT_TOKEN=<your-token>`
    ```
    ```
     vault read -format=json  sys/internal/counters/activity > output.json
    ```
    ```
     vault read -format=json  sys/internal/counters/activity/monthly > output_monthly.json
    ```
  - Vault UI
      
      ![Guide](https://github.com/hashicorp-dach/vault-usage-parser/blob/main/Guide.gif "Guide")
