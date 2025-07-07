import logging
import logging
logger = logging.getLogger(__name__)
from datetime import date, datetime



def main():
    # logging.basicConfig(filename='myapp.log', level=logging.INFO)
    # 로깅 기본 설정 (스크립트 시작 시 한 번만 호출)
    
    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S' # 예: 2025-04-22 10:07:49


    logging.basicConfig(filename='myapp.log',  level=logging.INFO, # INFO 레벨 이상만 기록
                        format=log_format,
                        datefmt=log_datefmt)
    logger.info('Started')
    logger.info('Finished')


if __name__ == '__main__':
    main()
    # 이제 로깅 함수 사용 가능
    logging.debug("상세 디버깅 정보입니다. (INFO 레벨 설정 시 출력 안 됨)")
    logging.info("프로그램이 시작되었습니다. (위치: Seoul)") # 위치 정보 활용
    logging.warning("설정 파일 (~/config.ini)을 찾을 수 없어 기본값을 사용합니다.")
    logging.error("데이터베이스 연결에 실패했습니다.")
    logging.critical("시스템의 주요 구성 요소가 작동하지 않습니다!")
