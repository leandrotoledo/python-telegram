#!/usr/bin/env python
# encoding: utf-8
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2016
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""
This module contains an object that represents Tests for JobQueue
"""
import logging
import sys
import unittest
import time
from time import sleep

from tests.test_updater import MockBot

sys.path.append('.')

from telegram.ext import JobQueue, Job, Updater
from telegram.ext.jobqueue import TimeUnits
from tests.base import BaseTest

# Enable logging
root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.WARN)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


class JobQueueTest(BaseTest, unittest.TestCase):
    """
    This object represents Tests for Updater, Dispatcher, WebhookServer and
    WebhookHandler
    """

    def setUp(self):
        self.jq = JobQueue(MockBot('jobqueue_test'))
        self.jq.start()
        self.result = 0
        self.job_time = 0

    def tearDown(self):
        if self.jq is not None:
            self.jq.stop()

    def getSeconds(self):
        return int(round(time.time()))

    def job1(self, bot, job):
        self.result += 1

    def job2(self, bot, job):
        raise Exception("Test Error")

    def job3(self, bot, job):
        self.result += 1
        job.schedule_removal()

    def job4(self, bot, job):
        self.result += job.context

    def job5(self, bot, job):
        self.job_time = self.getSeconds()

    def test_basic(self):
        self.jq.put(Job(self.job1, 0.1))
        sleep(1.5)
        self.assertGreaterEqual(self.result, 10)

    def test_job_with_context(self):
        self.jq.put(Job(self.job4, 0.1, context=5))
        sleep(1.5)
        self.assertGreaterEqual(self.result, 50)

    def test_noRepeat(self):
        self.jq.put(Job(self.job1, 0.1, repeat=False))
        sleep(0.5)
        self.assertEqual(1, self.result)

    def test_nextT(self):
        self.jq.put(Job(self.job1, 0.1), next_t=0.5)
        sleep(0.45)
        self.assertEqual(0, self.result)
        sleep(0.1)
        self.assertEqual(1, self.result)

    def test_multiple(self):
        self.jq.put(Job(self.job1, 0.1, repeat=False))
        self.jq.put(Job(self.job1, 0.2, repeat=False))
        self.jq.put(Job(self.job1, 0.4))
        sleep(1)
        self.assertEqual(4, self.result)

    def test_disabled(self):
        j0 = Job(self.job1, 0.1)
        j1 = Job(self.job1, 0.2)

        self.jq.put(j0)
        self.jq.put(Job(self.job1, 0.4))
        self.jq.put(j1)

        j0.enabled = False
        j1.enabled = False

        sleep(1)
        self.assertEqual(2, self.result)

    def test_schedule_removal(self):
        j0 = Job(self.job1, 0.1)
        j1 = Job(self.job1, 0.2)

        self.jq.put(j0)
        self.jq.put(Job(self.job1, 0.4))
        self.jq.put(j1)

        j0.schedule_removal()
        j1.schedule_removal()

        sleep(1)
        self.assertEqual(2, self.result)

    def test_schedule_removal_from_within(self):
        self.jq.put(Job(self.job1, 0.4))
        self.jq.put(Job(self.job3, 0.2))

        sleep(1)
        self.assertEqual(3, self.result)

    def test_longer_first(self):
        self.jq.put(Job(self.job1, 0.2, repeat=False))
        self.jq.put(Job(self.job1, 0.1, repeat=False))
        sleep(0.15)
        self.assertEqual(1, self.result)

    def test_error(self):
        self.jq.put(Job(self.job2, 0.1))
        self.jq.put(Job(self.job1, 0.2))
        sleep(0.5)
        self.assertEqual(2, self.result)

    def test_jobs_tuple(self):
        self.jq.stop()
        jobs = tuple(Job(self.job1, t) for t in range(5, 25))

        for job in jobs:
            self.jq.put(job)

        self.assertTupleEqual(jobs, self.jq.jobs())

    def test_inUpdater(self):
        u = Updater(bot="MockBot")
        u.job_queue.start()
        try:
            u.job_queue.put(Job(self.job1, 0.5))
            sleep(0.75)
            self.assertEqual(1, self.result)
            u.stop()
            sleep(2)
            self.assertEqual(1, self.result)
        finally:
            u.stop()

    def test_time_units(self):
        # I'm going to make all intervals about 5 seconds long
        # Testing the seconds time unit (it's default)
        seconds_interval = 5
        expected_time = self.getSeconds() + seconds_interval

        self.jq.put(Job(self.job5, seconds_interval, repeat=False))
        sleep(6)
        self.assertEqual(expected_time, self.job_time)

        # Testing the minute time unit
        minutes_interval = 0.083  # This is about 4.9 seconds
        expected_time = int(round(self.getSeconds() + (minutes_interval * 60)))

        self.jq.put(Job(self.job5, minutes_interval, repeat=False,
                        unit=TimeUnits.minutes))
        sleep(6)
        self.assertEqual(expected_time, self.job_time)

        # Testing the hour time unit
        hours_interval = 0.001389  # This is about 5.0004 seconds
        expected_time = int(round(self.getSeconds() + (hours_interval * 60 * 60)))

        self.jq.put(Job(self.job5, hours_interval, repeat=False,
                        unit=TimeUnits.hours))
        sleep(6)
        self.assertEqual(expected_time, self.job_time)


if __name__ == '__main__':
    unittest.main()
