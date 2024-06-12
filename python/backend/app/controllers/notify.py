def vmdeploy_slack_notify(output):
    images = {
        "RHEL": "https://www.cnet.com/a/img/hub/2009/06/30/61ac6620-f8e0-11e2-8c7c-d4ae52e62bcc/Red_Hat_-_Logo.jpg",
        "UBUNTU": "https://imageio.forbes.com/blogs-images/jasonevangelho/files/2018/07/ubuntu-logo.jpg?format=jpg&height=900&width=1600&fit=bounds",
        "CENTOS": "https://www.shapeblue.com/wp-content/uploads/2020/10/centos-logo-1.jpg",
        "ROCKY": "https://samba.plus/fileadmin/_processed_/e/b/csm_Rocky_Linux_97c0115185.png",
        "OTHERS": "https://api.slack.com/img/blocks/bkb_template_images/approvalsNewDevice.png",
    }

    # message block
    status_indicator = (
        ":white_check_mark:" if output["status"] == True else ":exclamation:"
    )

    slack_data = {
        "blocks": [
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"VM Number - {output['index']}"},
                    {
                        "type": "mrkdwn",
                        "text": f"Deployment Status - {output['status']} {status_indicator}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"Requested Hostname - *{output['variables']['fqdn']}*",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"Assigned IP Address - *{output['variables']['ipv4addr']}*",
                    },
                ],
                "accessory": {
                    "type": "image",
                    "image_url": images[output["variables"]["tags"][1]],
                    "alt_text": "os thumbnail",
                },
            },
        ],
        "attachments": [
            {
                "color": "#00FF00" if output["status"] == True else "#FF0000",
                "blocks": [
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*{output['ticket_ref']}* ticket raised by *{output['users']['requestor']}*",
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"Job Executed By - *{output['users']['executor']}*",
                            },
                        ],
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View Details",
                            },
                            "style": (
                                "primary" if output["status"] == True else "danger"
                            ),
                            "url": f"{output['job_url']}",
                        },
                    }
                ],
            }
        ],
    }

    return slack_data
