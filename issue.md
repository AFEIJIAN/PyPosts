# How to submit issue


## Navigation
- [Vulnerability](#vulnerability)
- [Bugs](#bugs)


## Vulnerability
- Vulnerability is used to report if any feature can be expose to hackers, dangerous, or can harm computers.
- Template can be view at [here](https://github.com/AFEIJIAN/PyPosts/blob/master/.github/ISSUE_TEMPLATE/vulnerability-report.md)

### Section `Vulnerability Basic Info`
- Basic info about the vulnerability
- Three categories to specify it:
  - Category
    - Category can be used:
      - `Server Internal` - Anything inside server, but not including operation that involves second or third user (e.g: client)
      - `External` - Anything that doesn't execute in server program, e.g: client authentication, client access
      - `Web` - Anything that related to the Web Management Panel
  - SubCategory 1
    - Category can be used:
      - `Operation` - Anything that **within the process** (base function) and **it is not a feature**, e.g: how communication between web server and client is a process, not a feature because **it is compulsory**
      - `Features` - Anything that isn't a base function, and not within a process, e.g: Auth Key Encryption is a feature because it isn't a **base function**, you may **also use `Features`** while you **unsure if this vulnerability is a features or operation**
  - SubCategory 2
    - Category can be used:
      - This can be anything you want
        - and it will describe the actual stuff you wanted to talk about, but must be related to `Category` and `SubCategory 1`
          - For example: if the `Category` is `Server Internal` and `SubCategory 1` is `Features`, then `SubCategory 2` should be related to Features of Server itself
            - e.g: `Auth Key as Basic Authentication`

### Section "Vulnerability Details Info"
- Detailed info about the vulnerability
  - "When will happen"
    - This describe what situation the vulnearability is used which become vulnerable, e.g: `When Auth Key stored in JavaScript script files.`
  - "How can this become vulnerable"
    - This explain why `When will happen` specified will become vulnerable, e.g: `JavaScript is client-side and Auth Key can be viewed via Browser Console.`
  - "Additional Info"
    - This can specify some recommendations or workaround to solve this vulnerability, or you can show some proofs from another sources to proves that this is vulnerable
      - Example of sources
        - Recommendations
          - Remove Auth Key Authentication
        - Proofs
          - [How do you protect an API key in JavaScript?](https://hashnode.com/post/how-do-you-protect-an-api-key-in-javascript-ciibz8foj01fqj3xtsyxbc5ga)
        - Workarounds
          - Remove Auth Key Authentication and turn server into implementable (Framework) for other program uses
Example of vulnerability report can be view at [here](https://github.com/AFEIJIAN/PyPosts/issues/1) (which is a vulnerability too!)
