from typing import List, Tuple
from base import Process

# 선점형 우선순위 스케줄링 함수
def Priority_Scheduler(processes: List[Process]) -> Tuple[List[Process], List[Tuple[str, int, int]]]:
    time = 0
    n = len(processes)
    completed = 0
    executions = []
    current_pid = None  # 현재 실행 중인 프로세스 ID
    start_time = None   # 현재 실행 중인 프로세스 시작 시간

    while completed < n:
        available = [p for p in processes if p.arrival_time <= time and not p.completed]
        if available:
            # 우선순위와 도착시간 기준으로 정렬 (작을수록 우선순위 높음)
            available.sort(key=lambda p: (p.priority, p.arrival_time))
            p = available[0]

            if current_pid != p.pid:
                if current_pid is not None:
                    executions.append((current_pid, start_time, time - start_time))
                current_pid = p.pid
                start_time = time

            if p.start_time == -1:
                p.start_time = time
                p.response_time = time - p.arrival_time

            p.remaining_time -= 1
            if p.remaining_time == 0:
                p.completed = True
                p.completion_time = time + 1
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.run_time
                completed += 1
        else:
            # 실행 가능한 프로세스 없으면 실행 기록 저장 후 대기 상태 초기화
            if current_pid is not None:
                executions.append((current_pid, start_time, time - start_time))
                current_pid = None
                start_time = None

        time += 1  # 시간 1 단위 증가

    if current_pid is not None:
        executions.append((current_pid, start_time, time - start_time))

    return processes, executions
