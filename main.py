from indeed import get_jobs as get_indeed_jobs
from saram import get_jobs as get_s_jobs
from save import save_to_file

indeed_jobs = get_indeed_jobs()
s_jobs = get_s_jobs()

jobs = s_jobs + indeed_jobs

save_to_file(jobs)
