# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from airflow import DAG
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="irs_990.irs_990_2015",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    irs_990_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="irs_990_transform_csv",
        startup_timeout_seconds=600,
        name="irs_990_2015",
        service_account_name="datasets",
        namespace="composer",
        image_pull_policy="Always",
        image="{{ var.json.irs_990.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.irs.gov/pub/irs-soi/15eofinextract990.dat.dat",
            "SOURCE_FILE": "files/data.dat",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/irs_990/irs_990_2015/data_output.csv",
            "PIPELINE_NAME": "irs_990_2015",
            "CSV_HEADERS": '["ein","elf","tax_pd","subseccd","s501c3or4947a1cd","schdbind","politicalactvtscd","lbbyingactvtscd","subjto6033cd","dnradvisedfundscd","prptyintrcvdcd","maintwrkofartcd","crcounselingqstncd","hldassetsintermpermcd","rptlndbldgeqptcd","rptinvstothsecd","rptinvstprgrelcd","rptothasstcd","rptothliabcd","sepcnsldtfinstmtcd","sepindaudfinstmtcd","inclinfinstmtcd","operateschools170cd","frgnofficecd","frgnrevexpnscd","frgngrntscd","frgnaggragrntscd","rptprofndrsngfeescd","rptincfnndrsngcd","rptincgamingcd","operatehosptlcd","hospaudfinstmtcd","rptgrntstogovtcd","rptgrntstoindvcd","rptyestocompnstncd","txexmptbndcd","invstproceedscd","maintescrwaccntcd","actonbehalfcd","engageexcessbnftcd","awarexcessbnftcd","loantofficercd","grantoofficercd","dirbusnreltdcd","fmlybusnreltdcd","servasofficercd","recvnoncashcd","recvartcd","ceaseoperationscd","sellorexchcd","ownsepentcd","reltdorgcd","intincntrlcd","orgtrnsfrcd","conduct5percentcd","compltschocd","f1096cnt","fw2gcnt","wthldngrulescd","noemplyeesw3cnt","filerqrdrtnscd","unrelbusinccd","filedf990tcd","frgnacctcd","prohibtdtxshltrcd","prtynotifyorgcd","filedf8886tcd","solicitcntrbcd","exprstmntcd","providegoodscd","notfydnrvalcd","filedf8282cd","f8282cnt","fndsrcvdcd","premiumspaidcd","filedf8899cd","filedf1098ccd","excbushldngscd","s4966distribcd","distribtodonorcd","initiationfees","grsrcptspublicuse","grsincmembers","grsincother","filedlieuf1041cd","txexmptint","qualhlthplncd","qualhlthreqmntn","qualhlthonhnd","rcvdpdtngcd","filedf720cd","totreprtabled","totcomprelatede","totestcompf","noindiv100kcnt","nocontractor100kcnt","totcntrbgfts","prgmservcode2acd","totrev2acola","prgmservcode2bcd","totrev2bcola","prgmservcode2ccd","totrev2ccola","prgmservcode2dcd","totrev2dcola","prgmservcode2ecd","totrev2ecola","totrev2fcola","totprgmrevnue","invstmntinc","txexmptbndsproceeds","royaltsinc","grsrntsreal","grsrntsprsnl","rntlexpnsreal","rntlexpnsprsnl","rntlincreal","rntlincprsnl","netrntlinc","grsalesecur","grsalesothr","cstbasisecur","cstbasisothr","gnlsecur","gnlsothr","netgnls","grsincfndrsng","lessdirfndrsng","netincfndrsng","grsincgaming","lessdirgaming","netincgaming","grsalesinvent","lesscstofgoods","netincsales","miscrev11acd","miscrevtota","miscrev11bcd","miscrevtot11b","miscrev11ccd","miscrevtot11c","miscrevtot11d","miscrevtot11e","totrevenue","grntstogovt","grnsttoindiv","grntstofrgngovt","benifitsmembrs","compnsatncurrofcr","compnsatnandothr","othrsalwages","pensionplancontrb","othremplyeebenef","payrolltx","feesforsrvcmgmt","legalfees","accntingfees","feesforsrvclobby","profndraising","feesforsrvcinvstmgmt","feesforsrvcothr","advrtpromo","officexpns","infotech","royaltsexpns","occupancy","travel","travelofpublicoffcl","converconventmtng","interestamt","pymtoaffiliates","deprcatndepletn","insurance","othrexpnsa","othrexpnsb","othrexpnsc","othrexpnsd","othrexpnse","othrexpnsf","totfuncexpns","nonintcashend","svngstempinvend","pldgegrntrcvblend","accntsrcvblend","currfrmrcvblend","rcvbldisqualend","notesloansrcvblend","invntriesalesend","prepaidexpnsend","lndbldgsequipend","invstmntsend","invstmntsothrend","invstmntsprgmend","intangibleassetsend","othrassetsend","totassetsend","accntspayableend","grntspayableend","deferedrevnuend","txexmptbndsend","escrwaccntliabend","paybletoffcrsend","secrdmrtgsend","unsecurednotesend","othrliabend","totliabend","unrstrctnetasstsend","temprstrctnetasstsend","permrstrctnetasstsend","capitalstktrstend","paidinsurplusend","retainedearnend","totnetassetend","totnetliabastend","nonpfrea","totnooforgscnt","totsupport","gftgrntsrcvd170","txrevnuelevied170","srvcsval170","pubsuppsubtot170","exceeds2pct170","pubsupplesspct170","samepubsuppsubtot170","grsinc170","netincunreltd170","othrinc170","totsupp170","grsrcptsrelated170","totgftgrntrcvd509","grsrcptsadmissn509","grsrcptsactivities509","txrevnuelevied509","srvcsval509","pubsuppsubtot509","rcvdfrmdisqualsub509","exceeds1pct509","subtotpub509","pubsupplesub509","samepubsuppsubtot509","grsinc509","unreltxincls511tx509","subtotsuppinc509","netincunrelatd509","othrinc509","totsupp509"]',
            "RENAME_MAPPINGS": '{"elf": "elf","EIN": "ein","tax_prd": "tax_pd","subseccd": "subseccd","s50Yc3or4947aYcd": "s501c3or4947a1cd","schdbind": "schdbind","politicalactvtscd": "politicalactvtscd","lbbyingactvtscd": "lbbyingactvtscd","subjto6033cd": "subjto6033cd","dnradvisedfundscd": "dnradvisedfundscd","prptyintrcvdcd": "prptyintrcvdcd","maintwrkofartcd": "maintwrkofartcd","crcounselingqstncd": "crcounselingqstncd","hldassetsintermpermcd": "hldassetsintermpermcd","rptlndbldgeqptcd": "rptlndbldgeqptcd","rptinvstothsecd": "rptinvstothsecd","rptinvstprgrelcd": "rptinvstprgrelcd","rptothasstcd": "rptothasstcd","rptothliabcd": "rptothliabcd","sepcnsldtfinstmtcd": "sepcnsldtfinstmtcd","sepindaudfinstmtcd": "sepindaudfinstmtcd","inclinfinstmtcd": "inclinfinstmtcd","operateschoolsY70cd": "operateschools170cd","frgnofficecd": "frgnofficecd","frgnrevexpnscd": "frgnrevexpnscd","frgngrntscd": "frgngrntscd","frgnaggragrntscd": "frgnaggragrntscd","rptprofndrsngfeescd": "rptprofndrsngfeescd","rptincfnndrsngcd": "rptincfnndrsngcd","rptincgamingcd": "rptincgamingcd","operatehosptlcd": "operatehosptlcd","hospaudfinstmtcd": "hospaudfinstmtcd","rptgrntstogovtcd": "rptgrntstogovtcd","rptgrntstoindvcd": "rptgrntstoindvcd","rptyestocompnstncd": "rptyestocompnstncd","txexmptbndcd": "txexmptbndcd","invstproceedscd": "invstproceedscd","maintescrwaccntcd": "maintescrwaccntcd","actonbehalfcd": "actonbehalfcd","engageexcessbnftcd": "engageexcessbnftcd","awarexcessbnftcd": "awarexcessbnftcd","loantofficercd": "loantofficercd","grantoofficercd": "grantoofficercd","dirbusnreltdcd": "dirbusnreltdcd","fmlybusnreltdcd": "fmlybusnreltdcd","servasofficercd": "servasofficercd","recvnoncashcd": "recvnoncashcd","recvartcd": "recvartcd","ceaseoperationscd": "ceaseoperationscd","sellorexchcd": "sellorexchcd","ownsepentcd": "ownsepentcd","reltdorgcd": "reltdorgcd","intincntrlcd": "intincntrlcd","orgtrnsfrcd": "orgtrnsfrcd","conduct5percentcd": "conduct5percentcd","compltschocd": "compltschocd","f1096cnt": "f1096cnt","fw2gcnt": "fw2gcnt","wthldngrulescd": "wthldngrulescd","noemplyeesw3cnt": "noemplyeesw3cnt","filerqrdrtnscd": "filerqrdrtnscd","unrelbusinccd": "unrelbusinccd","filedf990tcd": "filedf990tcd","frgnacctcd": "frgnacctcd","prohibtdtxshltrcd": "prohibtdtxshltrcd","prtynotifyorgcd": "prtynotifyorgcd","filedf8886tcd": "filedf8886tcd","solicitcntrbcd": "solicitcntrbcd","exprstmntcd": "exprstmntcd","providegoodscd": "providegoodscd","notfydnrvalcd": "notfydnrvalcd","filedf8N8Ncd": "filedf8282cd","f8282cnt": "f8282cnt","fndsrcvdcd": "fndsrcvdcd","premiumspaidcd": "premiumspaidcd","filedf8899cd": "filedf8899cd","filedfY098ccd": "filedf1098ccd","excbushldngscd": "excbushldngscd","s4966distribcd": "s4966distribcd","distribtodonorcd": "distribtodonorcd","initiationfees": "initiationfees","grsrcptspublicuse": "grsrcptspublicuse","grsincmembers": "grsincmembers","grsincother": "grsincother","filedlieufY04Ycd": "filedlieuf1041cd","txexmptint": "txexmptint","qualhlthplncd": "qualhlthplncd","qualhlthreqmntn": "qualhlthreqmntn","qualhlthonhnd": "qualhlthonhnd","rcvdpdtngcd": "rcvdpdtngcd","filedf7N0cd": "filedf720cd","totreprtabled": "totreprtabled","totcomprelatede": "totcomprelatede","totestcompf": "totestcompf","noindiv100kcnt": "noindiv100kcnt","nocontractor100kcnt": "nocontractor100kcnt","totcntrbgfts": "totcntrbgfts","prgmservcode2acd": "prgmservcode2acd","totrev2acola": "totrev2acola","prgmservcode2bcd": "prgmservcode2bcd","totrev2bcola": "totrev2bcola","prgmservcode2ccd": "prgmservcode2ccd","totrev2ccola": "totrev2ccola","prgmservcode2dcd": "prgmservcode2dcd","totrev2dcola": "totrev2dcola","prgmservcode2ecd": "prgmservcode2ecd","totrev2ecola": "totrev2ecola","totrev2fcola": "totrev2fcola","totprgmrevnue": "totprgmrevnue","invstmntinc": "invstmntinc","txexmptbndsproceeds": "txexmptbndsproceeds","royaltsinc": "royaltsinc","grsrntsreal": "grsrntsreal","grsrntsprsnl": "grsrntsprsnl","rntlexpnsreal": "rntlexpnsreal","rntlexpnsprsnl": "rntlexpnsprsnl","rntlincreal": "rntlincreal","rntlincprsnl": "rntlincprsnl","netrntlinc": "netrntlinc","grsalesecur": "grsalesecur","grsalesothr": "grsalesothr","cstbasisecur": "cstbasisecur","cstbasisothr": "cstbasisothr","gnlsecur": "gnlsecur","gnlsothr": "gnlsothr","netgnls": "netgnls","grsincfndrsng": "grsincfndrsng","lessdirfndrsng": "lessdirfndrsng","netincfndrsng": "netincfndrsng","grsincgaming": "grsincgaming","lessdirgaming": "lessdirgaming","netincgaming": "netincgaming","grsalesinvent": "grsalesinvent","lesscstofgoods": "lesscstofgoods","netincsales": "netincsales","miscrev11acd": "miscrev11acd","miscrevtota": "miscrevtota","miscrev11bcd": "miscrev11bcd","miscrevtot11b": "miscrevtot11b","miscrev11ccd": "miscrev11ccd","miscrevtot11c": "miscrevtot11c","miscrevtot11d": "miscrevtot11d","miscrevtot11e": "miscrevtot11e","totrevenue": "totrevenue","grntstogovt": "grntstogovt","grnsttoindiv": "grnsttoindiv","grntstofrgngovt": "grntstofrgngovt","benifitsmembrs": "benifitsmembrs","compnsatncurrofcr": "compnsatncurrofcr","compnsatnandothr": "compnsatnandothr","othrsalwages": "othrsalwages","pensionplancontrb": "pensionplancontrb","othremplyeebenef": "othremplyeebenef","payrolltx": "payrolltx","feesforsrvcmgmt": "feesforsrvcmgmt","legalfees": "legalfees","accntingfees": "accntingfees","feesforsrvclobby": "feesforsrvclobby","profndraising": "profndraising","feesforsrvcinvstmgmt": "feesforsrvcinvstmgmt","feesforsrvcothr": "feesforsrvcothr","advrtpromo": "advrtpromo","officexpns": "officexpns","infotech": "infotech","royaltsexpns": "royaltsexpns","occupancy": "occupancy","travel": "travel","travelofpublicoffcl": "travelofpublicoffcl","converconventmtng": "converconventmtng","interestamt": "interestamt","pymtoaffiliates": "pymtoaffiliates","deprcatndepletn": "deprcatndepletn","insurance": "insurance","othrexpnsa": "othrexpnsa","othrexpnsb": "othrexpnsb","othrexpnsc": "othrexpnsc","othrexpnsd": "othrexpnsd","othrexpnse": "othrexpnse","othrexpnsf": "othrexpnsf","totfuncexpns": "totfuncexpns","nonintcashend": "nonintcashend","svngstempinvend": "svngstempinvend","pldgegrntrcvblend": "pldgegrntrcvblend","accntsrcvblend": "accntsrcvblend","currfrmrcvblend": "currfrmrcvblend","rcvbldisqualend": "rcvbldisqualend","notesloansrcvblend": "notesloansrcvblend","invntriesalesend": "invntriesalesend","prepaidexpnsend": "prepaidexpnsend","lndbldgsequipend": "lndbldgsequipend","invstmntsend": "invstmntsend","invstmntsothrend": "invstmntsothrend","invstmntsprgmend": "invstmntsprgmend","intangibleassetsend": "intangibleassetsend","othrassetsend": "othrassetsend","totassetsend": "totassetsend","accntspayableend": "accntspayableend","grntspayableend": "grntspayableend","deferedrevnuend": "deferedrevnuend","txexmptbndsend": "txexmptbndsend","escrwaccntliabend": "escrwaccntliabend","paybletoffcrsend": "paybletoffcrsend","secrdmrtgsend": "secrdmrtgsend","unsecurednotesend": "unsecurednotesend","othrliabend": "othrliabend","totliabend": "totliabend","unrstrctnetasstsend": "unrstrctnetasstsend","temprstrctnetasstsend": "temprstrctnetasstsend","permrstrctnetasstsend": "permrstrctnetasstsend","capitalstktrstend": "capitalstktrstend","paidinsurplusend": "paidinsurplusend","retainedearnend": "retainedearnend","totnetassetend": "totnetassetend","totnetliabastend": "totnetliabastend","nonpfrea": "nonpfrea","totnooforgscnt": "totnooforgscnt","totsupport": "totsupport","gftgrntsrcvd170": "gftgrntsrcvd170","txrevnuelevied170": "txrevnuelevied170","srvcsval170": "srvcsval170","pubsuppsubtot170": "pubsuppsubtot170","exceeds2pct170": "exceeds2pct170","pubsupplesspct170": "pubsupplesspct170","samepubsuppsubtot170": "samepubsuppsubtot170","grsinc170": "grsinc170","netincunreltd170": "netincunreltd170","othrinc170": "othrinc170","totsupp170": "totsupp170","grsrcptsrelated170": "grsrcptsrelated170","totgftgrntrcvd509": "totgftgrntrcvd509","grsrcptsadmissn509": "grsrcptsadmissn509","grsrcptsactivities509": "grsrcptsactivities509","txrevnuelevied509": "txrevnuelevied509","srvcsval509": "srvcsval509","pubsuppsubtot509": "pubsuppsubtot509","rcvdfrmdisqualsub509": "rcvdfrmdisqualsub509","exceeds1pct509": "exceeds1pct509","subtotpub509": "subtotpub509","pubsupplesub509": "pubsupplesub509","samepubsuppsubtot509": "samepubsuppsubtot509","grsinc509": "grsinc509","unreltxincls511tx509": "unreltxincls511tx509","subtotsuppinc509": "subtotsuppinc509","netincunrelatd509": "netincunrelatd509","othrinc509": "othrinc509","totsupp509": "totsupp509"}',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_irs_990_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_irs_990_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/irs_990/irs_990_2015/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="irs_990.irs_990_2015",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "ein", "type": "string", "mode": "required"},
            {"name": "elf", "type": "string", "mode": "nullable"},
            {"name": "tax_pd", "type": "integer", "mode": "nullable"},
            {"name": "subseccd", "type": "integer", "mode": "nullable"},
            {"name": "s501c3or4947a1cd", "type": "string", "mode": "nullable"},
            {"name": "schdbind", "type": "string", "mode": "nullable"},
            {"name": "politicalactvtscd", "type": "string", "mode": "nullable"},
            {"name": "lbbyingactvtscd", "type": "string", "mode": "nullable"},
            {"name": "subjto6033cd", "type": "string", "mode": "nullable"},
            {"name": "dnradvisedfundscd", "type": "string", "mode": "nullable"},
            {"name": "prptyintrcvdcd", "type": "string", "mode": "nullable"},
            {"name": "maintwrkofartcd", "type": "string", "mode": "nullable"},
            {"name": "crcounselingqstncd", "type": "string", "mode": "nullable"},
            {"name": "hldassetsintermpermcd", "type": "string", "mode": "nullable"},
            {"name": "rptlndbldgeqptcd", "type": "string", "mode": "nullable"},
            {"name": "rptinvstothsecd", "type": "string", "mode": "nullable"},
            {"name": "rptinvstprgrelcd", "type": "string", "mode": "nullable"},
            {"name": "rptothasstcd", "type": "string", "mode": "nullable"},
            {"name": "rptothliabcd", "type": "string", "mode": "nullable"},
            {"name": "sepcnsldtfinstmtcd", "type": "string", "mode": "nullable"},
            {"name": "sepindaudfinstmtcd", "type": "string", "mode": "nullable"},
            {"name": "inclinfinstmtcd", "type": "string", "mode": "nullable"},
            {"name": "operateschools170cd", "type": "string", "mode": "nullable"},
            {"name": "frgnofficecd", "type": "string", "mode": "nullable"},
            {"name": "frgnrevexpnscd", "type": "string", "mode": "nullable"},
            {"name": "frgngrntscd", "type": "string", "mode": "nullable"},
            {"name": "frgnaggragrntscd", "type": "string", "mode": "nullable"},
            {"name": "rptprofndrsngfeescd", "type": "string", "mode": "nullable"},
            {"name": "rptincfnndrsngcd", "type": "string", "mode": "nullable"},
            {"name": "rptincgamingcd", "type": "string", "mode": "nullable"},
            {"name": "operatehosptlcd", "type": "string", "mode": "nullable"},
            {"name": "hospaudfinstmtcd", "type": "string", "mode": "nullable"},
            {"name": "rptgrntstogovtcd", "type": "string", "mode": "nullable"},
            {"name": "rptgrntstoindvcd", "type": "string", "mode": "nullable"},
            {"name": "rptyestocompnstncd", "type": "string", "mode": "nullable"},
            {"name": "txexmptbndcd", "type": "string", "mode": "nullable"},
            {"name": "invstproceedscd", "type": "string", "mode": "nullable"},
            {"name": "maintescrwaccntcd", "type": "string", "mode": "nullable"},
            {"name": "actonbehalfcd", "type": "string", "mode": "nullable"},
            {"name": "engageexcessbnftcd", "type": "string", "mode": "nullable"},
            {"name": "awarexcessbnftcd", "type": "string", "mode": "nullable"},
            {"name": "loantofficercd", "type": "string", "mode": "nullable"},
            {"name": "grantoofficercd", "type": "string", "mode": "nullable"},
            {"name": "dirbusnreltdcd", "type": "string", "mode": "nullable"},
            {"name": "fmlybusnreltdcd", "type": "string", "mode": "nullable"},
            {"name": "servasofficercd", "type": "string", "mode": "nullable"},
            {"name": "recvnoncashcd", "type": "string", "mode": "nullable"},
            {"name": "recvartcd", "type": "string", "mode": "nullable"},
            {"name": "ceaseoperationscd", "type": "string", "mode": "nullable"},
            {"name": "sellorexchcd", "type": "string", "mode": "nullable"},
            {"name": "ownsepentcd", "type": "string", "mode": "nullable"},
            {"name": "reltdorgcd", "type": "string", "mode": "nullable"},
            {"name": "intincntrlcd", "type": "string", "mode": "nullable"},
            {"name": "orgtrnsfrcd", "type": "string", "mode": "nullable"},
            {"name": "conduct5percentcd", "type": "string", "mode": "nullable"},
            {"name": "compltschocd", "type": "string", "mode": "nullable"},
            {"name": "f1096cnt", "type": "integer", "mode": "nullable"},
            {"name": "fw2gcnt", "type": "integer", "mode": "nullable"},
            {"name": "wthldngrulescd", "type": "string", "mode": "nullable"},
            {"name": "noemplyeesw3cnt", "type": "integer", "mode": "nullable"},
            {"name": "filerqrdrtnscd", "type": "string", "mode": "nullable"},
            {"name": "unrelbusinccd", "type": "string", "mode": "nullable"},
            {"name": "filedf990tcd", "type": "string", "mode": "nullable"},
            {"name": "frgnacctcd", "type": "string", "mode": "nullable"},
            {"name": "prohibtdtxshltrcd", "type": "string", "mode": "nullable"},
            {"name": "prtynotifyorgcd", "type": "string", "mode": "nullable"},
            {"name": "filedf8886tcd", "type": "string", "mode": "nullable"},
            {"name": "solicitcntrbcd", "type": "string", "mode": "nullable"},
            {"name": "exprstmntcd", "type": "string", "mode": "nullable"},
            {"name": "providegoodscd", "type": "string", "mode": "nullable"},
            {"name": "notfydnrvalcd", "type": "string", "mode": "nullable"},
            {"name": "filedf8282cd", "type": "string", "mode": "nullable"},
            {"name": "f8282cnt", "type": "integer", "mode": "nullable"},
            {"name": "fndsrcvdcd", "type": "string", "mode": "nullable"},
            {"name": "premiumspaidcd", "type": "string", "mode": "nullable"},
            {"name": "filedf8899cd", "type": "string", "mode": "nullable"},
            {"name": "filedf1098ccd", "type": "string", "mode": "nullable"},
            {"name": "excbushldngscd", "type": "string", "mode": "nullable"},
            {"name": "s4966distribcd", "type": "string", "mode": "nullable"},
            {"name": "distribtodonorcd", "type": "string", "mode": "nullable"},
            {"name": "initiationfees", "type": "integer", "mode": "nullable"},
            {"name": "grsrcptspublicuse", "type": "integer", "mode": "nullable"},
            {"name": "grsincmembers", "type": "integer", "mode": "nullable"},
            {"name": "grsincother", "type": "integer", "mode": "nullable"},
            {"name": "filedlieuf1041cd", "type": "string", "mode": "nullable"},
            {"name": "txexmptint", "type": "integer", "mode": "nullable"},
            {"name": "qualhlthplncd", "type": "string", "mode": "nullable"},
            {"name": "qualhlthreqmntn", "type": "integer", "mode": "nullable"},
            {"name": "qualhlthonhnd", "type": "integer", "mode": "nullable"},
            {"name": "rcvdpdtngcd", "type": "string", "mode": "nullable"},
            {"name": "filedf720cd", "type": "string", "mode": "nullable"},
            {"name": "totreprtabled", "type": "integer", "mode": "nullable"},
            {"name": "totcomprelatede", "type": "integer", "mode": "nullable"},
            {"name": "totestcompf", "type": "integer", "mode": "nullable"},
            {"name": "noindiv100kcnt", "type": "integer", "mode": "nullable"},
            {"name": "nocontractor100kcnt", "type": "integer", "mode": "nullable"},
            {"name": "totcntrbgfts", "type": "integer", "mode": "nullable"},
            {"name": "prgmservcode2acd", "type": "integer", "mode": "nullable"},
            {"name": "totrev2acola", "type": "integer", "mode": "nullable"},
            {"name": "prgmservcode2bcd", "type": "integer", "mode": "nullable"},
            {"name": "totrev2bcola", "type": "integer", "mode": "nullable"},
            {"name": "prgmservcode2ccd", "type": "integer", "mode": "nullable"},
            {"name": "totrev2ccola", "type": "integer", "mode": "nullable"},
            {"name": "prgmservcode2dcd", "type": "integer", "mode": "nullable"},
            {"name": "totrev2dcola", "type": "integer", "mode": "nullable"},
            {"name": "prgmservcode2ecd", "type": "integer", "mode": "nullable"},
            {"name": "totrev2ecola", "type": "integer", "mode": "nullable"},
            {"name": "totrev2fcola", "type": "integer", "mode": "nullable"},
            {"name": "totprgmrevnue", "type": "integer", "mode": "nullable"},
            {"name": "invstmntinc", "type": "integer", "mode": "nullable"},
            {"name": "txexmptbndsproceeds", "type": "integer", "mode": "nullable"},
            {"name": "royaltsinc", "type": "integer", "mode": "nullable"},
            {"name": "grsrntsreal", "type": "integer", "mode": "nullable"},
            {"name": "grsrntsprsnl", "type": "integer", "mode": "nullable"},
            {"name": "rntlexpnsreal", "type": "integer", "mode": "nullable"},
            {"name": "rntlexpnsprsnl", "type": "integer", "mode": "nullable"},
            {"name": "rntlincreal", "type": "integer", "mode": "nullable"},
            {"name": "rntlincprsnl", "type": "integer", "mode": "nullable"},
            {"name": "netrntlinc", "type": "integer", "mode": "nullable"},
            {"name": "grsalesecur", "type": "integer", "mode": "nullable"},
            {"name": "grsalesothr", "type": "integer", "mode": "nullable"},
            {"name": "cstbasisecur", "type": "integer", "mode": "nullable"},
            {"name": "cstbasisothr", "type": "integer", "mode": "nullable"},
            {"name": "gnlsecur", "type": "integer", "mode": "nullable"},
            {"name": "gnlsothr", "type": "integer", "mode": "nullable"},
            {"name": "netgnls", "type": "integer", "mode": "nullable"},
            {"name": "grsincfndrsng", "type": "integer", "mode": "nullable"},
            {"name": "lessdirfndrsng", "type": "integer", "mode": "nullable"},
            {"name": "netincfndrsng", "type": "integer", "mode": "nullable"},
            {"name": "grsincgaming", "type": "integer", "mode": "nullable"},
            {"name": "lessdirgaming", "type": "integer", "mode": "nullable"},
            {"name": "netincgaming", "type": "integer", "mode": "nullable"},
            {"name": "grsalesinvent", "type": "integer", "mode": "nullable"},
            {"name": "lesscstofgoods", "type": "integer", "mode": "nullable"},
            {"name": "netincsales", "type": "integer", "mode": "nullable"},
            {"name": "miscrev11acd", "type": "integer", "mode": "nullable"},
            {"name": "miscrevtota", "type": "integer", "mode": "nullable"},
            {"name": "miscrev11bcd", "type": "integer", "mode": "nullable"},
            {"name": "miscrevtot11b", "type": "integer", "mode": "nullable"},
            {"name": "miscrev11ccd", "type": "integer", "mode": "nullable"},
            {"name": "miscrevtot11c", "type": "integer", "mode": "nullable"},
            {"name": "miscrevtot11d", "type": "integer", "mode": "nullable"},
            {"name": "miscrevtot11e", "type": "integer", "mode": "nullable"},
            {"name": "totrevenue", "type": "integer", "mode": "nullable"},
            {"name": "grntstogovt", "type": "integer", "mode": "nullable"},
            {"name": "grnsttoindiv", "type": "integer", "mode": "nullable"},
            {"name": "grntstofrgngovt", "type": "integer", "mode": "nullable"},
            {"name": "benifitsmembrs", "type": "integer", "mode": "nullable"},
            {"name": "compnsatncurrofcr", "type": "integer", "mode": "nullable"},
            {"name": "compnsatnandothr", "type": "integer", "mode": "nullable"},
            {"name": "othrsalwages", "type": "integer", "mode": "nullable"},
            {"name": "pensionplancontrb", "type": "integer", "mode": "nullable"},
            {"name": "othremplyeebenef", "type": "integer", "mode": "nullable"},
            {"name": "payrolltx", "type": "integer", "mode": "nullable"},
            {"name": "feesforsrvcmgmt", "type": "integer", "mode": "nullable"},
            {"name": "legalfees", "type": "integer", "mode": "nullable"},
            {"name": "accntingfees", "type": "integer", "mode": "nullable"},
            {"name": "feesforsrvclobby", "type": "integer", "mode": "nullable"},
            {"name": "profndraising", "type": "integer", "mode": "nullable"},
            {"name": "feesforsrvcinvstmgmt", "type": "integer", "mode": "nullable"},
            {"name": "feesforsrvcothr", "type": "integer", "mode": "nullable"},
            {"name": "advrtpromo", "type": "integer", "mode": "nullable"},
            {"name": "officexpns", "type": "integer", "mode": "nullable"},
            {"name": "infotech", "type": "integer", "mode": "nullable"},
            {"name": "royaltsexpns", "type": "integer", "mode": "nullable"},
            {"name": "occupancy", "type": "integer", "mode": "nullable"},
            {"name": "travel", "type": "integer", "mode": "nullable"},
            {"name": "travelofpublicoffcl", "type": "integer", "mode": "nullable"},
            {"name": "converconventmtng", "type": "integer", "mode": "nullable"},
            {"name": "interestamt", "type": "integer", "mode": "nullable"},
            {"name": "pymtoaffiliates", "type": "integer", "mode": "nullable"},
            {"name": "deprcatndepletn", "type": "integer", "mode": "nullable"},
            {"name": "insurance", "type": "integer", "mode": "nullable"},
            {"name": "othrexpnsa", "type": "integer", "mode": "nullable"},
            {"name": "othrexpnsb", "type": "integer", "mode": "nullable"},
            {"name": "othrexpnsc", "type": "integer", "mode": "nullable"},
            {"name": "othrexpnsd", "type": "integer", "mode": "nullable"},
            {"name": "othrexpnse", "type": "integer", "mode": "nullable"},
            {"name": "othrexpnsf", "type": "integer", "mode": "nullable"},
            {"name": "totfuncexpns", "type": "integer", "mode": "nullable"},
            {"name": "nonintcashend", "type": "integer", "mode": "nullable"},
            {"name": "svngstempinvend", "type": "integer", "mode": "nullable"},
            {"name": "pldgegrntrcvblend", "type": "integer", "mode": "nullable"},
            {"name": "accntsrcvblend", "type": "integer", "mode": "nullable"},
            {"name": "currfrmrcvblend", "type": "integer", "mode": "nullable"},
            {"name": "rcvbldisqualend", "type": "integer", "mode": "nullable"},
            {"name": "notesloansrcvblend", "type": "integer", "mode": "nullable"},
            {"name": "invntriesalesend", "type": "integer", "mode": "nullable"},
            {"name": "prepaidexpnsend", "type": "integer", "mode": "nullable"},
            {"name": "lndbldgsequipend", "type": "integer", "mode": "nullable"},
            {"name": "invstmntsend", "type": "integer", "mode": "nullable"},
            {"name": "invstmntsothrend", "type": "integer", "mode": "nullable"},
            {"name": "invstmntsprgmend", "type": "integer", "mode": "nullable"},
            {"name": "intangibleassetsend", "type": "integer", "mode": "nullable"},
            {"name": "othrassetsend", "type": "integer", "mode": "nullable"},
            {"name": "totassetsend", "type": "integer", "mode": "nullable"},
            {"name": "accntspayableend", "type": "integer", "mode": "nullable"},
            {"name": "grntspayableend", "type": "integer", "mode": "nullable"},
            {"name": "deferedrevnuend", "type": "integer", "mode": "nullable"},
            {"name": "txexmptbndsend", "type": "integer", "mode": "nullable"},
            {"name": "escrwaccntliabend", "type": "integer", "mode": "nullable"},
            {"name": "paybletoffcrsend", "type": "integer", "mode": "nullable"},
            {"name": "secrdmrtgsend", "type": "integer", "mode": "nullable"},
            {"name": "unsecurednotesend", "type": "integer", "mode": "nullable"},
            {"name": "othrliabend", "type": "integer", "mode": "nullable"},
            {"name": "totliabend", "type": "integer", "mode": "nullable"},
            {"name": "unrstrctnetasstsend", "type": "integer", "mode": "nullable"},
            {"name": "temprstrctnetasstsend", "type": "integer", "mode": "nullable"},
            {"name": "permrstrctnetasstsend", "type": "integer", "mode": "nullable"},
            {"name": "capitalstktrstend", "type": "integer", "mode": "nullable"},
            {"name": "paidinsurplusend", "type": "integer", "mode": "nullable"},
            {"name": "retainedearnend", "type": "integer", "mode": "nullable"},
            {"name": "totnetassetend", "type": "integer", "mode": "nullable"},
            {"name": "totnetliabastend", "type": "integer", "mode": "nullable"},
            {"name": "nonpfrea", "type": "integer", "mode": "nullable"},
            {"name": "totnooforgscnt", "type": "integer", "mode": "nullable"},
            {"name": "totsupport", "type": "integer", "mode": "nullable"},
            {"name": "gftgrntsrcvd170", "type": "integer", "mode": "nullable"},
            {"name": "txrevnuelevied170", "type": "integer", "mode": "nullable"},
            {"name": "srvcsval170", "type": "integer", "mode": "nullable"},
            {"name": "pubsuppsubtot170", "type": "integer", "mode": "nullable"},
            {"name": "exceeds2pct170", "type": "integer", "mode": "nullable"},
            {"name": "pubsupplesspct170", "type": "integer", "mode": "nullable"},
            {"name": "samepubsuppsubtot170", "type": "integer", "mode": "nullable"},
            {"name": "grsinc170", "type": "integer", "mode": "nullable"},
            {"name": "netincunreltd170", "type": "integer", "mode": "nullable"},
            {"name": "othrinc170", "type": "integer", "mode": "nullable"},
            {"name": "totsupp170", "type": "integer", "mode": "nullable"},
            {"name": "grsrcptsrelated170", "type": "integer", "mode": "nullable"},
            {"name": "totgftgrntrcvd509", "type": "integer", "mode": "nullable"},
            {"name": "grsrcptsadmissn509", "type": "integer", "mode": "nullable"},
            {"name": "grsrcptsactivities509", "type": "integer", "mode": "nullable"},
            {"name": "txrevnuelevied509", "type": "integer", "mode": "nullable"},
            {"name": "srvcsval509", "type": "integer", "mode": "nullable"},
            {"name": "pubsuppsubtot509", "type": "integer", "mode": "nullable"},
            {"name": "rcvdfrmdisqualsub509", "type": "integer", "mode": "nullable"},
            {"name": "exceeds1pct509", "type": "integer", "mode": "nullable"},
            {"name": "subtotpub509", "type": "integer", "mode": "nullable"},
            {"name": "pubsupplesub509", "type": "integer", "mode": "nullable"},
            {"name": "samepubsuppsubtot509", "type": "integer", "mode": "nullable"},
            {"name": "grsinc509", "type": "integer", "mode": "nullable"},
            {"name": "unreltxincls511tx509", "type": "integer", "mode": "nullable"},
            {"name": "subtotsuppinc509", "type": "integer", "mode": "nullable"},
            {"name": "netincunrelatd509", "type": "integer", "mode": "nullable"},
            {"name": "othrinc509", "type": "integer", "mode": "nullable"},
            {"name": "totsupp509", "type": "integer", "mode": "nullable"},
        ],
    )

    irs_990_transform_csv >> load_irs_990_to_bq
